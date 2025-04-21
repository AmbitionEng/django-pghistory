# Settings

Below are all settings for `django-pghistory`.

## Middlware and Context Tracking

#### PGHISTORY_MIDDLEWARE_METHODS

Set the HTTP methods tracked by the middleware.

*Default* `("GET", "POST", "PUT", "PATCH", "DELETE")`

#### PGHISTORY_JSON_ENCODER

The JSON encoder class or class path to use when serializing context.

*Default* `"django.core.serializers.json.DjangoJSONEncoder"`

#### PGHISTORY_INSTALL_CONTEXT_FUNC_ON_MIGRATE

Install the Postgres `_pgh_attach_context` function after migrations. Ensures pghistory context tracking works even without running migrations, typically for test suites.

*Default* `False`

## Event Models and Trackers

#### PGHISTORY_APPEND_ONLY

If event models should be append-only by default.

*Default* `False`

#### PGHISTORY_BASE_MODEL

The base model to use for event models.

*Default* `pghistory.models.Event`

#### PGHISTORY_CONTEXT_FIELD

The default configuration for the `pgh_context` field.

*Default* `pghistory.ContextForeignKey()`

#### PGHISTORY_CONTEXT_ID_FIELD

The default configuration for the `pgh_context_id` field when [pghistory.ContextJSONField][] is used for the `pgh_context` field.

*Default* `pghistory.ContextUUIDField()`

#### PGHISTORY_CREATED_AT_FUNCTION

Pghistory uses `NOW()` to determine the current time, which is the same timestamp for the entire transaction. Configure this setting to `CLOCK_TIMESTAMP()`, for example, if you'd like to use a different SQL function for determining the current time.

*Default* `"NOW()"`

#### PGHISTORY_DEFAULT_TRACKERS

The default trackers to use for event models.

*Default* `(pghistory.InsertEvent(), pghistory.UpdateEvent())`

#### PGHISTORY_FIELD

The default configuration for fields in event models.

*Default* `pghistory.Field()`

#### PGHISTORY_FOREIGN_KEY_FIELD

The default configuration for foreign keys in event models.

*Default* `pghistory.ForeignKey()`

#### PGHISTORY_LEVEL

The default trigger level for [pghistory.RowEvent][] trackers.

*Default* `pghistory.Row`

#### PGHISTORY_OBJ_FIELD

The default configuration for the `pgh_obj` field.

*Default* `pghistory.ObjForeignKey()`

#### PGHISTORY_RELATED_FIELD

The default configuration for related fields in event models.

*Default* `pghistory.RelatedField()`

<a id="exclude_field_kwargs"></a>
#### PGHISTORY_EXCLUDE_FIELD_KWARGS

When creating fields for the event model, new fields are supplied with argument overrides. Sometimes this can result in an incorrect keyword argument being provided to a field. For example, `primary_key` fails Django's check framework when passed to an `ImageField`.

Use this setting to ignore certain keyword arguments being passed to child field instances.

The setting is a dictionary where the key is the field class or a string to a class path, and the value is a list of arguments to ignore. For example, `{models.ImageField: ["primary_key"]}`.

*Default* `{}`

!!! note

    The primary key example for image fields is already handled and does not need to be configured.

## Admin

#### PGHISTORY_ADMIN_ALL_EVENTS

`True` if all events should be able to be displayed in the default Django `Events` admin page without filtering.

*Default* `True`

#### PGHISTORY_ADMIN_CLASS

The admin class to use. Must subclass [pghistory.admin.EventsAdmin][].

*Default* `"pghistory.admin.EventsAdmin"`

#### PGHISTORY_ADMIN_MODEL

The default model or model label for the `Events` admin.

*Default* `"pghistory.Events"`

#### PGHISTORY_ADMIN_ORDERING

The default ordering for the `Events` admin.

*Default* `"-pgh_created_at"`

#### PGHISTORY_ADMIN_LIST_DISPLAY

The default fields shown in the `Events` admin.

*Default* `["pgh_created_at", "pgh_obj_model", "pgh_obj_id", "pgh_diff"]`. If `pghistory.MiddlewareEvents` is the event model, the "user" and "url" fields will be added.

#### PGHISTORY_ADMIN_QUERYSET

The default queryset for the `Events` admin. If set, `PGHISTORY_ADMIN_MODEL` will be ignored.

*Default* Uses `PGHISTORY_ADMIN_MODEL` ordered by `PGHISTORY_ADMIN_ORDERING`.
