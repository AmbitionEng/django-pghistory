import ddf
import pytest
from django.db import connection

import pghistory.runtime
import pghistory.tests.models as test_models
import pghistory.utils


@pytest.mark.parametrize(
    "statement, expected",
    [
        ("create index concurrently", True),
        ("create index", True),
        ("select * from auth_user", True),
        ("vacuum table", True),
        ("analyze table", True),
        ("checkpoint table", True),
        ("discard all", True),
        ("load extension", True),
        ("cluster", True),
        ("update auth_user set id= %s where id = %s", False),
        (b"create index concurrently", True),
        (b"select * from auth_user", True),
        (b"update auth_user set id= %s where id = %s", False),
        ("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ", True),
        ("set transaction isolation level read committed", True),
        ("SET TRANSACTION READ ONLY", True),
        ("set transaction read write", True),
        ("SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL SERIALIZABLE", True),
        ("BEGIN", True),
        ("begin transaction", True),
        ("START TRANSACTION", True),
        ("start transaction isolation level repeatable read", True),
        ("SELECT * FROM table", True),
        ("INSERT INTO table VALUES (1)", False),
        ("UPDATE table SET col = 1", False),
        ("DELETE FROM table", False),
        ("SET search_path = public", False),
        (b"SET TRANSACTION ISOLATION LEVEL REPEATABLE READ", True),
        (b"SELECT * FROM table", True),
    ],
)
def test_is_ignored_statement(statement, expected):
    assert pghistory.runtime._is_ignored_statement(statement) == expected


@pytest.mark.skipif(
    pghistory.utils.psycopg_maj_version == 3, reason="Psycopg2 preserves entire query"
)
@pytest.mark.django_db
@pytest.mark.parametrize(
    "sql, params",
    [
        ("update auth_user set id= %s where id = %s", (1, 1)),
        ("update auth_user set id= %(id1)s where id = %(id2)s", {"id1": 1, "id2": 1}),
        (b"update auth_user set id= %s where id = %s", (1, 1)),
        (b"update auth_user set id= %(id1)s where id = %(id2)s", {"id1": 1, "id2": 1}),
    ],
)
def test_inject_history_context(settings, mocker, sql, params):
    mocker.patch("uuid.uuid4", return_value="uuid", autospec=True)
    settings.DEBUG = True
    expected_sql = "SELECT set_config('pghistory.context_id', 'uuid', true), set_config('pghistory.context_metadata', '{\"hello\": \"world\"}', true);"  # noqa
    with pghistory.context(hello="world"):
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            query = connection.queries[-1]
            assert query["sql"].startswith(expected_sql)


@pytest.mark.django_db
def test_inject_history_context_composed_sql():
    """psycopg's sql.Composable is valid for cursor.execute, so context injection must accept it"""
    if pghistory.utils.psycopg_maj_version == 3:
        from psycopg import sql
    else:
        from psycopg2 import sql

    obj = ddf.G(test_models.EventModel)
    query = sql.SQL("UPDATE {} SET int_field = %s WHERE id = %s").format(
        sql.Identifier(test_models.EventModel._meta.db_table)
    )
    with pghistory.context() as ctx:
        with connection.cursor() as cursor:
            cursor.execute(query, (obj.int_field + 1, obj.id))

    assert obj.events.get(pgh_label="before_update").pgh_context_id == ctx.id
