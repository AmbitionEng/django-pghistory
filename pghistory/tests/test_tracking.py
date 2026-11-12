import uuid

import ddf
import pytest
from django.db import connection, transaction

import pghistory.models
import pghistory.tests.models as test_models


@pytest.mark.django_db
@pytest.mark.parametrize(
    "context_id, metadata",
    [
        (None, None),
        (None, "{}"),
        ("00000000-0000-0000-0000-000000000001", None),
        ("", ""),
        ("", "{}"),
        ("00000000-0000-0000-0000-000000000001", ""),
        ("invalid-uuid", "{}"),
        ("00000000-0000-0000-0000-000000000001", "invalid-json"),
    ],
)
def test_attach_context_missing_or_invalid(context_id, metadata):
    """Missing, reset, partial, and malformed settings do not create context."""
    # A new connection distinguishes settings that have never existed from
    # custom settings that PostgreSQL resets to empty strings after a transaction.
    isolated_connection = connection.copy()
    try:
        with isolated_connection.cursor() as cursor:
            cursor.execute(
                "SELECT current_setting('pghistory.context_id', TRUE), "
                "current_setting('pghistory.context_metadata', TRUE)"
            )
            assert cursor.fetchone() == (None, None)
            if context_id is not None:
                cursor.execute(
                    "SELECT set_config('pghistory.context_id', %s, FALSE)", [context_id]
                )
            if metadata is not None:
                cursor.execute(
                    "SELECT set_config('pghistory.context_metadata', %s, FALSE)", [metadata]
                )
            cursor.execute("SELECT _pgh_attach_context()")
            assert cursor.fetchone() == (None,)
    finally:
        isolated_connection.close()

    assert not pghistory.models.Context.objects.exists()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "metadata, expected",
    [("{}", {}), ("null", None), ('{"user":1}', {"user": 1}), ('""', ""), ("[]", [])],
)
def test_attach_context_valid_metadata(metadata, expected):
    """An empty object and JSON null remain valid context metadata."""
    context_id = uuid.uuid4()
    with connection.cursor() as cursor:
        cursor.execute("SELECT set_config('pghistory.context_id', %s, TRUE)", [str(context_id)])
        cursor.execute("SELECT set_config('pghistory.context_metadata', %s, TRUE)", [metadata])
        cursor.execute("SELECT _pgh_attach_context()")
        assert cursor.fetchone() == (context_id,)

    context = pghistory.models.Context.objects.get()
    assert context.id == context_id
    assert context.metadata == expected


@pytest.mark.django_db
def test_attach_context_preserves_noop_and_updates():
    """Reattaching unchanged context does not update the row or its timestamp."""
    with pghistory.context(user=1) as ctx:
        ddf.G(test_models.EventModel)
        context = pghistory.models.Context.objects.get()
        original_created_at = context.created_at
        original_updated_at = context.updated_at
        with connection.cursor() as cursor:
            cursor.execute("SELECT ctid::text FROM pghistory_context WHERE id = %s", [ctx.id])
            original_ctid = cursor.fetchone()[0]
            cursor.execute("SELECT _pgh_attach_context()")
            assert cursor.fetchone() == (ctx.id,)
            cursor.execute("SELECT ctid::text FROM pghistory_context WHERE id = %s", [ctx.id])
            assert cursor.fetchone()[0] == original_ctid

        context.refresh_from_db()
        assert context.created_at == original_created_at
        assert context.updated_at == original_updated_at

        with pghistory.context(user=2):
            ddf.G(test_models.EventModel)
        context.refresh_from_db()
        assert context.metadata == {"user": 2}
        assert context.created_at == original_created_at
        # NOW() retains the existing transaction-time timestamp semantics.
        assert context.updated_at == original_updated_at


@pytest.mark.django_db
def test_attach_context_rolls_back_with_event():
    """The fast path preserves the transaction boundary for context and events."""
    with pghistory.context(user=1):
        with pytest.raises(ValueError, match="rollback"):
            with transaction.atomic():
                ddf.G(test_models.EventModel)
                assert pghistory.models.Context.objects.count() == 1
                raise ValueError("rollback")

    assert not pghistory.models.Context.objects.exists()
    assert not test_models.EventModel.objects.exists()
    assert all(
        not event_model.objects.exists()
        for event_model in set(test_models.EventModel.pgh_event_models.values())
    )


@pytest.mark.django_db
def test_attach_context_update_rolls_back_with_event():
    """Rolling back a later event also restores the existing context metadata."""
    with pghistory.context(user=1):
        model = ddf.G(test_models.EventModel)
        with pytest.raises(ValueError, match="rollback"):
            with transaction.atomic(), pghistory.context(user=2):
                model.int_field += 1
                model.save()
                assert pghistory.models.Context.objects.get().metadata == {"user": 2}
                raise ValueError("rollback")

    assert pghistory.models.Context.objects.get().metadata == {"user": 1}
    assert model.events.count() == 1


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_async_context():
    async with pghistory.context(example="context"):
        dummy = await test_models.BigAutoFieldModel.objects.acreate()

    event = await test_models.BigAutoFieldModel.pgh_event_model.objects.select_related(
        "pgh_context"
    ).aget()
    assert event.pgh_obj_id == dummy.id
    assert event.pgh_context is not None
    assert event.pgh_context.metadata == {"example": "context"}

    # async pytest django does not clean up the database. Clean up manually
    await test_models.BigAutoFieldModel.pgh_event_model.objects.all().adelete()
    await test_models.BigAutoFieldModel.objects.all().adelete()
    await pghistory.models.Context.objects.all().adelete()


@pytest.mark.django_db(transaction=True)
def test_concurrent_index_creation():
    """
    Verify that context tracking works even when creating
    concurrent indices. This operation is not compatible with
    context tracking and should be ignored
    """
    with pghistory.context(key1="val1"):
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                CREATE INDEX   CONCURRENTLY IF NOT EXISTS idx_name ON
                {test_models.SnapshotModel._meta.db_table}
                (dt_field)
            """
            )


@pytest.mark.django_db
def test_named_cursor():
    """
    Verify that context tracking still works when a named
    cursor is used. Named cursors are used in Django when using
    .iterator()
    """
    with pghistory.context(key1="val1") as ctx:
        # Creating the EventModel will trigger an event, which will
        # attach the current context
        ddf.G("tests.EventModel")

        ctx1 = pghistory.models.Context.objects.get()
        assert ctx1.id == ctx.id
        assert ctx1.metadata == {"key1": "val1"}

        for val in test_models.EventModel.objects.iterator():
            assert val


@pytest.mark.django_db()
@pytest.mark.parametrize("event_model", [test_models.EventModel, test_models.EventModelStatement])
def test_scope_inside_transaction(event_model):
    """
    Tests some characteristics of context scope when in a transaction
    """
    # No context should be attached at first
    no_ctx = ddf.G(event_model)
    assert no_ctx.events.get().pgh_context_id is None

    # Attach context
    with pghistory.context() as ctx:
        with_ctx = ddf.G(event_model)
        assert with_ctx.events.get().pgh_context_id == ctx.id

    # Although we are out of the context manager, we are still in
    # a transaction, so local context variables will still persist
    with_local_ctx = ddf.G(event_model)
    assert with_local_ctx.events.get().pgh_context_id == ctx.id


@pytest.mark.django_db
@pytest.mark.parametrize("event_model", [test_models.EventModel, test_models.EventModelStatement])
def test_track_context_id(mocker, event_model):
    """
    Verifies the tracker attaches a context uuid
    """
    with pghistory.context() as ctx:
        m = ddf.G(event_model)
        orig_dt = m.dt_field
        orig_int = m.int_field

        assert list(m.events.values()) == [
            {
                "pgh_created_at": mocker.ANY,
                "pgh_context_id": ctx.id,
                "dt_field": orig_dt,
                "pgh_id": mocker.ANY,
                "pgh_label": "model.create",
                "int_field": orig_int,
                "pgh_obj_id": m.id,
                "id": m.id,
            }
        ]


@pytest.mark.django_db
def test_track_context_metadata_single_quote(mocker):
    """
    Verifies that context metadata with single quotes is properly
    escaped
    """
    with pghistory.context(
        key1="can't",
        key2="''quoted''",
    ) as ctx:
        # Creating the EventModel will trigger an event, which will
        # attach the current context
        ddf.G("tests.EventModel")

    ctx1 = pghistory.models.Context.objects.get()
    assert ctx1.id == ctx.id
    assert ctx1.metadata == {
        "key1": "can't",
        "key2": "''quoted''",
    }


@pytest.mark.django_db
def test_track_context_metadata_percent(mocker):
    """
    Verifies that context metadata with single quotes is properly
    escaped
    """
    with pghistory.context(key="%s") as ctx:
        # Creating the EventModel will trigger an event, which will
        # attach the current context
        ddf.G("tests.EventModel")

    ctx1 = pghistory.models.Context.objects.get()
    assert ctx1.id == ctx.id
    assert ctx1.metadata == {"key": "%s"}


@pytest.mark.django_db
@pytest.mark.parametrize("event_model", [test_models.EventModel, test_models.EventModelStatement])
def test_track_context_metadata(mocker, event_model):
    """
    Verifies that the proper metadata is attached to a tracked event
    """
    with pghistory.context(key1="val1") as ctx:
        # Creating the EventModel will trigger an event, which will
        # attach the current context
        m1 = ddf.G(event_model, int_field=1)

        ctx1 = pghistory.models.Context.objects.get()
        assert ctx1.id == ctx.id
        assert ctx1.metadata == {"key1": "val1"}

        # Attach additional metadata
        with pghistory.context(key2="val2"):
            # Perform another event so that context will be flushed
            m1.int_field = 2
            m1.save()

            ctx1.refresh_from_db()
            assert ctx1.id == ctx.id
            assert ctx1.metadata == {"key1": "val1", "key2": "val2"}

        # Even after exiting inner context, the metadata persists until
        # the end of the outer context
        m1.int_field = 3
        m1.save()
        ctx1.refresh_from_db()
        assert ctx1.id == ctx.id
        assert ctx1.metadata == {"key1": "val1", "key2": "val2"}

    # Starting a new tracking session will result in a new context object
    with pghistory.context() as ctx:
        ddf.G(event_model)
        assert pghistory.models.Context.objects.count() == 2
        ctx2 = pghistory.models.Context.objects.exclude(id=ctx1.id).get()
        assert ctx2.id == ctx.id
        assert ctx2.metadata == {}


@pytest.mark.django_db
@pytest.mark.parametrize("event_model", [test_models.EventModel, test_models.EventModelStatement])
def test_nested_tracking(mocker, event_model):
    """
    Verifies the tracker can be nested many times without issue
    """
    with pghistory.context() as ctx:
        with pghistory.context() as nested_ctx:
            assert ctx.id == nested_ctx.id
            m = ddf.G(event_model, int_field=2)

            assert list(m.events.values()) == [
                {
                    "pgh_created_at": mocker.ANY,
                    "pgh_context_id": ctx.id,
                    "dt_field": m.dt_field,
                    "pgh_id": mocker.ANY,
                    "pgh_label": "model.create",
                    "int_field": m.int_field,
                    "pgh_obj_id": m.id,
                    "id": m.id,
                }
            ]

        m.int_field = 3
        m.save()

        assert list(m.events.values().order_by("pgh_id")) == [
            {
                "pgh_created_at": mocker.ANY,
                "pgh_context_id": ctx.id,
                "dt_field": m.dt_field,
                "pgh_id": mocker.ANY,
                "pgh_label": "model.create",
                "int_field": 2,
                "pgh_obj_id": m.id,
                "id": m.id,
            },
            {
                "pgh_created_at": mocker.ANY,
                "pgh_context_id": ctx.id,
                "dt_field": m.dt_field,
                "pgh_id": mocker.ANY,
                "pgh_label": "before_update",
                "int_field": 2,
                "pgh_obj_id": m.id,
                "id": m.id,
            },
        ]
