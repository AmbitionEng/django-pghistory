import pytest
from django.db import connection

import pghistory.runtime
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
