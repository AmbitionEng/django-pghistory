# Troubleshooting

If you have issues with the triggers that are installed by `django-pghistory`, we recommend reading [django-pgtrigger's troubleshooting guide](https://django-pgtrigger.readthedocs.io/en/latest/troubleshooting/). It goes over most of the core issues that might happen when creating or migrating triggers.

## A tracked field cannot be created

Special fields, such as Django's `ImageField` cannot be supplied some of the core field parameter overrides supplied, such as the `primary_key` attribute.

If a custom field errors because of invalid arguments, use `settings.PGHISTORY_EXCLUDE_FIELD_KWARGS`. See the [settings section here](settings.md#exclude_field_kwargs) for an example.

## Migrating to denormalized context

If migrating existing models to use [denormalized context](event_models.md#denormalizing-context) through the setting (`PGHISTORY_CONTEXT_FIELD = pghistory.ContextJSONField()`) or through arguments to [pghistory.track][] (`context_field=pghistory.ContextJSONField()`), you'll hit [this issue](https://github.com/AmbitionEng/django-pghistory/issues/218) and need to manually modify your migrations.

To address this, first generate migrations as normal. You'll see the following migration operations in your file:

```python
migrations.AddField(
    model_name="...",
    name="pgh_context",
    field=pghistory.utils.JSONField(null=True),
),
migrations.AlterField(
    model_name="...",
    name="pgh_context_id",
    field=models.UUIDField(null=True),
),
```

Your migration needs to remove the `pgh_context` field first and add the field instead of altering it later:

```python hl_lines="1-4 10"
migrations.RemoveField(
    model_name="...",
    name="pgh_context",
),
migrations.AddField(
    model_name="...",
    name="pgh_context",
    field=pghistory.utils.JSONField(null=True),
),
migrations.AddField(
    model_name="...",
    name="pgh_context_id",
    field=models.UUIDField(null=True),
),
```

Another way to accomplish this without manually editing migrations is to set the context field to `None`, generate migrations, and then set it to the denormalized context field.
