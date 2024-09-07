# Generated by Django 4.2.6 on 2024-09-07 01:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pghistory", "0006_delete_aggregateevent"),
        (
            "tests",
            "0011_ignoreautofieldssnapshotmodelcreatedatupdatedatmycharfieldmyintfieldevent_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="bigautofieldmodelevent",
            name="pgh_context",
            field=models.ForeignKey(
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="pghistory.context",
            ),
        ),
        migrations.AlterField(
            model_name="bigautofieldmodelevent",
            name="pgh_obj",
            field=models.ForeignKey(
                db_constraint=False,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="events",
                to="tests.bigautofieldmodel",
            ),
        ),
        migrations.AlterField(
            model_name="customeventmodel",
            name="pgh_obj",
            field=models.ForeignKey(
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="custom_related_name",
                to="tests.eventmodel",
            ),
        ),
        migrations.AlterField(
            model_name="customeventwithcontext",
            name="pgh_context",
            field=models.ForeignKey(
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="pghistory.context",
            ),
        ),
        migrations.AlterField(
            model_name="customeventwithcontext",
            name="pgh_obj",
            field=models.ForeignKey(
                db_constraint=False,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="tests.eventmodel",
            ),
        ),
        migrations.AlterField(
            model_name="custommodelevent",
            name="pgh_context",
            field=models.ForeignKey(
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="pghistory.context",
            ),
        ),
        migrations.AlterField(
            model_name="custommodelevent",
            name="pgh_obj",
            field=models.ForeignKey(
                db_constraint=False,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="events",
                to="tests.custommodel",
            ),
        ),
        migrations.AlterField(
            model_name="custommodelsnapshot",
            name="pgh_context",
            field=models.ForeignKey(
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="pghistory.context",
            ),
        ),
        migrations.AlterField(
            model_name="custommodelsnapshot",
            name="pgh_obj",
            field=models.ForeignKey(
                db_constraint=False,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="snapshot",
                to="tests.custommodel",
            ),
        ),
        migrations.AlterField(
            model_name="customsnapshotmodel",
            name="pgh_obj",
            field=models.ForeignKey(
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="custom_related_name",
                to="tests.snapshotmodel",
            ),
        ),
        migrations.AlterField(
            model_name="denormcontextevent",
            name="pgh_obj",
            field=models.ForeignKey(
                db_constraint=False,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="events",
                to="tests.denormcontext",
            ),
        ),
        migrations.AlterField(
            model_name="denormcontexteventnoid",
            name="pgh_obj",
            field=models.ForeignKey(
                db_constraint=False,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="event_no_id",
                to="tests.denormcontext",
            ),
        ),
        migrations.AlterField(
            model_name="eventmodelevent",
            name="pgh_context",
            field=models.ForeignKey(
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="pghistory.context",
            ),
        ),
        migrations.AlterField(
            model_name="eventmodelevent",
            name="pgh_obj",
            field=models.ForeignKey(
                db_constraint=False,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="events",
                to="tests.eventmodel",
            ),
        ),
        migrations.AlterField(
            model_name="ignoreautofieldssnapshotmodelcreatedatupdatedatmycharfieldmyintfieldevent",
            name="pgh_context",
            field=models.ForeignKey(
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="pghistory.context",
            ),
        ),
        migrations.AlterField(
            model_name="ignoreautofieldssnapshotmodelcreatedatupdatedatmycharfieldmyintfieldevent",
            name="pgh_obj",
            field=models.ForeignKey(
                db_constraint=False,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="no_auto_fields_event",
                to="tests.ignoreautofieldssnapshotmodel",
            ),
        ),
        migrations.AlterField(
            model_name="nopghobjevent",
            name="pgh_context",
            field=models.ForeignKey(
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="pghistory.context",
            ),
        ),
        migrations.AlterField(
            model_name="nopghobjsnapshot",
            name="pgh_context",
            field=models.ForeignKey(
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="pghistory.context",
            ),
        ),
        migrations.AlterField(
            model_name="snapshotimagefieldevent",
            name="pgh_context",
            field=models.ForeignKey(
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="pghistory.context",
            ),
        ),
        migrations.AlterField(
            model_name="snapshotimagefieldevent",
            name="pgh_obj",
            field=models.ForeignKey(
                db_constraint=False,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="events",
                to="tests.snapshotimagefield",
            ),
        ),
        migrations.AlterField(
            model_name="snapshotmodeldtfieldevent",
            name="pgh_context",
            field=models.ForeignKey(
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="pghistory.context",
            ),
        ),
        migrations.AlterField(
            model_name="snapshotmodeldtfieldevent",
            name="pgh_obj",
            field=models.ForeignKey(
                db_constraint=False,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="dt_field_snapshot",
                to="tests.snapshotmodel",
            ),
        ),
        migrations.AlterField(
            model_name="snapshotmodeldtfieldintfieldevent",
            name="pgh_context",
            field=models.ForeignKey(
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="pghistory.context",
            ),
        ),
        migrations.AlterField(
            model_name="snapshotmodeldtfieldintfieldevent",
            name="pgh_obj",
            field=models.ForeignKey(
                db_constraint=False,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="dt_field_int_field_snapshot",
                to="tests.snapshotmodel",
            ),
        ),
        migrations.AlterField(
            model_name="snapshotmodelsnapshot",
            name="pgh_context",
            field=models.ForeignKey(
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="pghistory.context",
            ),
        ),
        migrations.AlterField(
            model_name="snapshotmodelsnapshot",
            name="pgh_obj",
            field=models.ForeignKey(
                db_constraint=False,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="snapshot",
                to="tests.snapshotmodel",
            ),
        ),
        migrations.AlterField(
            model_name="snapshotuntrackedfield",
            name="pgh_context",
            field=models.ForeignKey(
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="pghistory.context",
            ),
        ),
        migrations.AlterField(
            model_name="snapshotuntrackedfield",
            name="pgh_obj",
            field=models.ForeignKey(
                db_constraint=False,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="untracked_field_event",
                to="tests.ignoreautofieldssnapshotmodel",
            ),
        ),
        migrations.AlterField(
            model_name="uniqueconstraintmodelevent",
            name="pgh_context",
            field=models.ForeignKey(
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="pghistory.context",
            ),
        ),
        migrations.AlterField(
            model_name="uniqueconstraintmodelevent",
            name="pgh_obj",
            field=models.ForeignKey(
                db_constraint=False,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="snapshot",
                to="tests.uniqueconstraintmodel",
            ),
        ),
        migrations.AlterField(
            model_name="usergroupsevent",
            name="pgh_context",
            field=models.ForeignKey(
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="pghistory.context",
            ),
        ),
    ]
