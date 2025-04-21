from django.contrib.auth.models import User
from django.db import models

import pghistory


@pghistory.track()
class SnapshotImageField(models.Model):
    img_field = models.ImageField()


class UntrackedModel(models.Model):
    untracked = models.CharField(max_length=64)


@pghistory.track()
class BigAutoFieldModel(models.Model):
    id = models.BigAutoField(primary_key=True)


class CustomAutoFieldModel(models.Model):
    id = models.AutoField(primary_key=True, db_column="pk_id")


class CustomBigAutoFieldModel(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="pk_id")


@pghistory.track(context_field=pghistory.ContextJSONField())
@pghistory.track(
    pghistory.InsertEvent("snapshot_no_id_insert"),
    pghistory.UpdateEvent("snapshot_no_id_update"),
    obj_field=pghistory.ObjForeignKey(related_name="event_no_id"),
    context_field=pghistory.ContextJSONField(),
    context_id_field=None,
    model_name="DenormContextEventNoId",
)
class DenormContext(models.Model):
    """
    For testing denormalized context
    """

    int_field = models.IntegerField()
    fk_field = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)


@pghistory.track(context_field=pghistory.ContextJSONField(), level=pghistory.Statement)
@pghistory.track(
    pghistory.InsertEvent("snapshot_no_id_insert"),
    pghistory.UpdateEvent("snapshot_no_id_update"),
    obj_field=pghistory.ObjForeignKey(related_name="event_no_id"),
    context_field=pghistory.ContextJSONField(),
    context_id_field=None,
    model_name="DenormContextEventNoIdStatement",
    level=pghistory.Statement,
)
class DenormContextStatement(models.Model):
    """
    For testing denormalized context with statement-level triggers
    """

    int_field = models.IntegerField()
    fk_field = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)


@pghistory.track(
    model_name="CustomModelSnapshot", obj_field=pghistory.ObjForeignKey(related_name="snapshot")
)
@pghistory.track(
    pghistory.UpdateEvent(
        "int_field_updated",
        condition=pghistory.AnyChange("int_field"),
    )
)
class CustomModel(models.Model):
    """
    For testing history tracking with a custom primary key
    and custom column name
    """

    my_pk = models.UUIDField(primary_key=True)
    int_field = models.IntegerField(db_column="integer_field")


@pghistory.track(obj_field=pghistory.ObjForeignKey(related_name="snapshot"), append_only=True)
class UniqueConstraintModel(models.Model):
    """For testing tracking models with unique constraints"""

    my_one_to_one = models.OneToOneField(CustomModel, on_delete=models.PROTECT)
    my_char_field = models.CharField(unique=True, max_length=32)
    my_int_field1 = models.IntegerField(db_index=True)
    my_int_field2 = models.IntegerField()

    class Meta:
        unique_together = [("my_int_field1", "my_int_field2")]


@pghistory.track(
    pghistory.InsertEvent("dt_field_snapshot_insert"),
    pghistory.UpdateEvent("dt_field_snapshot_update"),
    fields=["dt_field"],
    obj_field=pghistory.ObjForeignKey(related_name="dt_field_snapshot"),
)
@pghistory.track(
    pghistory.InsertEvent("dt_field_int_field_snapshot_insert"),
    pghistory.UpdateEvent("dt_field_int_field_snapshot_update"),
    fields=["dt_field", "int_field"],
    obj_field=pghistory.ObjForeignKey(related_name="dt_field_int_field_snapshot"),
)
@pghistory.track(
    pghistory.InsertEvent("snapshot_insert"),
    pghistory.UpdateEvent("snapshot_update"),
    model_name="SnapshotModelSnapshot",
    obj_field=pghistory.ObjForeignKey(related_name="snapshot"),
)
@pghistory.track(
    pghistory.InsertEvent("no_pgh_obj_snapshot_insert"),
    pghistory.UpdateEvent("no_pgh_obj_snapshot_update"),
    model_name="NoPghObjSnapshot",
    obj_field=None,
)
class SnapshotModel(models.Model):
    """
    For testing snapshots of a model or fields
    """

    dt_field = models.DateTimeField()
    int_field = models.IntegerField()
    fk_field = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)


class CustomSnapshotModel(
    pghistory.create_event_model(
        SnapshotModel,
        pghistory.InsertEvent("custom_snapshot_insert"),
        pghistory.UpdateEvent("custom_snapshot_update"),
        exclude=["dt_field"],
        obj_field=pghistory.ObjForeignKey(
            related_name="custom_related_name",
            null=True,
            on_delete=models.SET_NULL,
        ),
        context_field=None,
    )
):
    fk_field = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True)
    # Add an extra field that's not on the original model to try to throw
    # tests off
    fk_field2 = models.ForeignKey(
        "auth.User",
        db_constraint=False,
        null=True,
        on_delete=models.DO_NOTHING,
        related_name="+",
        related_query_name="+",
    )


@pghistory.track(
    pghistory.ManualEvent("manual_event"),
    pghistory.InsertEvent("model.create"),
    pghistory.UpdateEvent("before_update", row=pghistory.Old),
    pghistory.DeleteEvent("before_delete", row=pghistory.Old),
    pghistory.UpdateEvent("after_update", condition=pghistory.AnyChange("dt_field")),
)
@pghistory.track(
    pghistory.Tracker("no_pgh_obj_manual_event"),
    obj_field=None,
    model_name="NoPghObjEvent",
)
class EventModel(models.Model):
    """
    For testing model events
    """

    dt_field = models.DateTimeField()
    int_field = models.IntegerField()


@pghistory.track(
    pghistory.ManualEvent("manual_event"),
    pghistory.InsertEvent("model.create"),
    pghistory.UpdateEvent("before_update", row=pghistory.Old),
    pghistory.DeleteEvent("before_delete", row=pghistory.Old),
    pghistory.UpdateEvent("after_update", condition=pghistory.AnyChange("dt_field")),
    level=pghistory.Statement,
    append_only=True,
)
@pghistory.track(
    pghistory.Tracker("no_pgh_obj_manual_event"),
    obj_field=None,
    model_name="NoPghObjEventStatement",
    level=pghistory.Statement,
    append_only=True,
)
class EventModelStatement(models.Model):
    """
    For testing model events with statement-level triggers
    """

    dt_field = models.DateTimeField()
    int_field = models.IntegerField()


@pghistory.track(
    pghistory.InsertEvent("int_field1_created", condition=pghistory.Q(new__int_field1__gt=100)),
    pghistory.UpdateEvent("int_field1_updated", condition=pghistory.AnyChange("int_field1")),
    pghistory.UpdateEvent(
        "int_field2_incr",
        condition=pghistory.Q(old__int_field2__lt=pghistory.F("new__int_field2")),
    ),
    pghistory.DeleteEvent("int_field1_deleted", condition=pghistory.Q(old__int_field1__lt=50)),
    level=pghistory.Statement,
)
class CondStatement(models.Model):
    """
    For testing conditional statement-level triggers
    """

    int_field1 = models.IntegerField()
    int_field2 = models.IntegerField()


class CustomEventModel(
    pghistory.create_event_model(
        EventModel,
        pghistory.InsertEvent("model.custom_create"),
        fields=["dt_field"],
        context_field=None,
        obj_field=pghistory.ObjForeignKey(
            related_name="custom_related_name",
            null=True,
            on_delete=models.SET_NULL,
        ),
    )
):
    pass


CustomEventWithContext = pghistory.create_event_model(
    EventModel,
    pghistory.InsertEvent("model.custom_create_with_context"),
    abstract=False,
    model_name="CustomEventWithContext",
    obj_field=pghistory.ObjForeignKey(related_name="+"),
)


class CustomEventProxy(EventModel.pgh_event_models["model.create"]):
    url = pghistory.ProxyField("pgh_context__metadata__url", models.TextField(null=True))
    auth_user = pghistory.ProxyField(
        "pgh_context__metadata__user",
        models.ForeignKey("auth.User", on_delete=models.DO_NOTHING, null=True),
    )

    class Meta:
        proxy = True


class CustomEvents(pghistory.models.Events):
    user = models.ForeignKey("auth.User", on_delete=models.DO_NOTHING, null=True)
    url = pghistory.ProxyField("pgh_context__url", models.TextField(null=True))

    class Meta:
        proxy = True


@pghistory.track(
    pghistory.InsertEvent("group.add"),
    pghistory.DeleteEvent("group.remove"),
    obj_field=None,
)
class UserGroups(User.groups.through):
    class Meta:
        proxy = True


@pghistory.track(
    pghistory.UpdateEvent(row=pghistory.Old, condition=pghistory.AnyChange(exclude_auto=True)),
    pghistory.DeleteEvent(),
    obj_field=pghistory.ObjForeignKey(related_name="no_auto_fields_event"),
    fields=["created_at", "updated_at", "my_char_field", "my_int_field"],
)
@pghistory.track(
    pghistory.UpdateEvent(
        "untracked_field", row=pghistory.Old, condition=pghistory.AnyChange("untracked_field")
    ),
    fields=["created_at", "updated_at", "my_char_field", "my_int_field"],
    obj_field=pghistory.ObjForeignKey(related_name="untracked_field_event"),
    model_name="SnapshotUntrackedField",
)
class IgnoreAutoFieldsSnapshotModel(models.Model):
    """For testing the IgnoreAutoFieldsSnapshot tracker"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    my_char_field = models.CharField(max_length=32)
    my_int_field = models.IntegerField()
    untracked_field = models.CharField(max_length=32)


class ConcreteParent(models.Model):
    name = models.CharField(max_length=32)


@pghistory.track()
class ConcreteChild(ConcreteParent):
    age = models.IntegerField()
