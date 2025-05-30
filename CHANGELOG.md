# Changelog

## 3.7.0 (2025-05-25)

#### Changes

  - Ignore appending tracking configuration to `SELECT` statements when tracking context by [@stephan0h](https://github.com/stephan0h) in [#207](https://github.com/AmbitionEng/django-pghistory/pull/207).
  - Fix typo in docs by [@BStephenBB](https://github.com/BStephenBB) in [#198](https://github.com/AmbitionEng/django-pghistory/pull/198).

## 3.6.0 (2025-04-21)

#### Improvements

  - Add support for statement-level history tracking triggers, offering substantial performance improvements for tracking history over bulk operations by [@wesleykendall](https://github.com/wesleykendall) in [#197](https://github.com/AmbitionEng/django-pghistory/pull/197).

    Use `@pghistory.track(level=pghistory.Statement)` to leverage statement-level triggers in history tracking. Set is as the default with `PGHISTORY_LEVEL = pghistory.Statement`.

    A usage guide was added to the "Performance and Scaling" section of the docs. It notes how it works with conditional history tracking and caveats to be aware of.

  - Optimize context tracking by [@wesleykendall](https://github.com/wesleykendall) in [#197](https://github.com/AmbitionEng/django-pghistory/pull/197).

    Context tracking in history triggers is significantly faster when there are many historical events in a span.

#### Changes

  - Add support for Django 5.2, drop support for Postgres 13 by [@wesleykendall](https://github.com/wesleykendall) in [#196](https://github.com/AmbitionEng/django-pghistory/pull/196).

## 3.5.5 (2025-03-27)

#### Changes

  - Allow passing extra context to the admin template by [@Mariatta](https://github.com/Mariatta) in [#192](https://github.com/AmbitionEng/django-pghistory/pull/192).

## 3.5.4 (2025-03-12)

#### Changes

  - Ensure generated fields on models are tracked properly by [@pmdevita](https://github.com/pmdevita) in [#187](https://github.com/AmbitionEng/django-pghistory/pull/187).

## 3.5.3 (2025-02-27)

#### Fixes

  - Fix custom field support by deconstructing field classes correctly in history model by [@iamsauravsharma](https://github.com/iamsauravsharma) in [#184](https://github.com/AmbitionEng/django-pghistory/pull/184).

## 3.5.2 (2025-02-05)

#### Changes

  - Ignore `test` command when tracking context [@iamsauravsharma](https://github.com/iamsauravsharma) in [#180](https://github.com/AmbitionEng/django-pghistory/pull/182).

## 3.5.1 (2024-12-15)

#### Changes

  - Changed project ownership to `AmbitionEng` by [@wesleykendall](https://github.com/wesleykendall) in [#180](https://github.com/AmbitionEng/django-pghistory/pull/180).

## 3.5.0 (2024-11-01)

### Features

  - Optimized `Events` diff queries by ~100x via a subquery instead of `LAG` windows by [@lokhman](https://github.com/lokhman) in [#173](https://github.com/Opus10/django-pghistory/pull/173).
  - Optimized object-level `Events` queries in the django admin by avoiding `UNION` queries by [@lokhman](https://github.com/lokhman) in [#174](https://github.com/Opus10/django-pghistory/pull/174).

### Changes

  - Added Python 3.13 support, dropped Python 3.8. Added Postgres17 support by [@wesleykendall](https://github.com/wesleykendall) in [#175](https://github.com/Opus10/django-pghistory/pull/175).

## 3.4.4 (2024-09-27)

#### Fixes

  - Fix db_column not being passed through on tracked AutoFields by [@pmdevita](https://github.com/pmdevita) in [#166](https://github.com/Opus10/django-pghistory/pull/168).

## 3.4.3 (2024-09-14)

#### Fixes

  - Add missing py.typed file by [@max-muoto](https://github.com/max-muoto) in [#166](https://github.com/Opus10/django-pghistory/pull/166).

## 3.4.2 (2024-09-10)

#### Fixes

- Fix using `@pghistory.track()` on models that have concrete inheritance by [@wesleykendall](https://github.com/wesleykendall) in [#164](https://github.com/Opus10/django-pghistory/pull/164).

## 3.4.1 (2024-09-06)

#### Fixes

- The `related_query_name` setting for tracked foreign keys had the default value mistakenly changed in v3.4.0. Fixed by [@wesleykendall](https://github.com/wesleykendall) in [#163](https://github.com/Opus10/django-pghistory/pull/163).

## 3.4.0 (2024-09-02)

#### Features

- Make context middleware extensible by [@wesleykendall](https://github.com/wesleykendall) in [#141](https://github.com/Opus10/django-pghistory/pull/141).

    Inherit `pghistory.context.HistoryMiddleware` and override `get_context` to add additional context data for every request.

- Support offline documentation formats by [@wesleykendall](https://github.com/wesleykendall) in [#144](https://github.com/Opus10/django-pghistory/pull/144).

    PDF versions of documentation are built via ReadTheDocs.

#### Fixes

- Check that the execute result is not `None` before trying to access `execute_result.nextset()` by [@wesleykendall](https://github.com/wesleykendall) in [#156](https://github.com/Opus10/django-pghistory/pull/156).
- Ensure `pghistory.create_event` works when using denormalized context by [@wesleykendall](https://github.com/wesleykendall) in [#154](https://github.com/Opus10/django-pghistory/pull/154).
- More accurate type hints for the public interface by [@wesleykendall](https://github.com/wesleykendall) in [#143](https://github.com/Opus10/django-pghistory/pull/143).
- Fix minor docstring issue in `pghistory.create_event_model` by [@wesleykendall](https://github.com/wesleykendall) in [#148](https://github.com/Opus10/django-pghistory/pull/148).

#### Documentation

- Clean up configuration section of docs, ensure all settings are documented by [@wesleykendall](https://github.com/wesleykendall) in [#142](https://github.com/Opus10/django-pghistory/pull/142).
- Modify conditional tracking examples by [@wesleykendall](https://github.com/wesleykendall) in [#145](https://github.com/Opus10/django-pghistory/pull/145).
- Add section to FAQ on backfilling data by [@wesleykendall](https://github.com/wesleykendall) in [#146](https://github.com/Opus10/django-pghistory/pull/146).
- Adjust guide on tracking management commands by [@wesleykendall](https://github.com/wesleykendall) in [#150](https://github.com/Opus10/django-pghistory/pull/150).
- Note the Q/A discussions in the FAQ by [@wesleykendall](https://github.com/wesleykendall) in [#152](https://github.com/Opus10/django-pghistory/pull/152).

## 3.3.0 (2024-08-27)

#### Features

- `PGHISTORY_INSTALL_CONTEXT_FUNC_ON_MIGRATE` setting to configure installation of tracking function after migrations by [@wesleykendall](https://github.com/wesleykendall) in [#140](https://github.com/Opus10/django-pghistory/pull/140).
- `PGHISTORY_CREATED_AT_FUNCTION` setting to configure the function for determining the current time in history triggers by [@lokhman](https://github.com/lokhman) in [#137](https://github.com/Opus10/django-pghistory/pull/137).
- Add ASGI support by [@pablogadhi](https://github.com/pablogadhi) in [#127](https://github.com/Opus10/django-pghistory/pull/127).

#### Fixes

- Ensure `BigAutoField`s are properly mirrored in history models by [@tobiasmcnulty](https://github.com/tobiasmcnulty) in [#134](https://github.com/Opus10/django-pghistory/pull/134).

    !!! warning

        If you have event models for models with `BigAutoField` primary keys, you will see new migrations to convert `pgh_obj_id` to a bigint.

- Support filtering event models by referenced proxy models by [@lokhman](https://github.com/lokhman) in [#135](https://github.com/Opus10/django-pghistory/pull/135).
- Ensure `bytes` representations of SQL are handled by [@tobiasmcnulty](https://github.com/tobiasmcnulty) in [#136](https://github.com/Opus10/django-pghistory/pull/136).
- Fix setting default trackers with the `PGHISTORY_DEFAULT_TRACKERS` setting by [@SupImDos](https://github.com/SupImDos) in [#133](https://github.com/Opus10/django-pghistory/pull/133).
- Don't install pghistory's context tracking function on non-postgres databases by [@pmdevita](https://github.com/pmdevita) in [#132](https://github.com/Opus10/django-pghistory/pull/132).
- Ensure `MiddlewareEvents` doesn't filter out non-middleware events in the admin by [@lokhman](https://github.com/lokhman) in [#130](https://github.com/Opus10/django-pghistory/pull/130).
- Support custom primary keys for the aggregate `Events` proxy model by [@lokhman](https://github.com/lokhman) in [#128](https://github.com/Opus10/django-pghistory/pull/128).
- Fix type hints for `pghistory.track` by [@SebastianDix](https://github.com/SebastianDix) in [#118](https://github.com/SebastianDix)[https://github.com/Opus10/django-pghistory/pull/118].
- Support named arguments in SQL by (@foobarna)[https://github.com/foobarna] in (#111)[https://github.com/Opus10/django-pghistory/pull/111].

#### Changes

- Django 5.1 compatibility, dropped Django 3.2 / Postgres 12 support by [@wesleykendall](https://github.com/wesleykendall) in [#139](https://github.com/Opus10/django-pghistory/pull/139).
- Added section in FAQ for handling issues with concrete inheritance by [@xaitec](https://github.com/xaitec) in [#138](https://github.com/Opus10/django-pghistory/pull/138).
- Add reference to DjangoCon talk in the docs by [@max-muoto](https://github.com/max-muoto) in [#114](https://github.com/Opus10/django-pghistory/pull/114).

## 3.2.0 (2024-04-20)

#### Bug

  - Fix Empty List being passed into create_event_model [Maxwell Muoto, b89c86d]

    Fix Empty List being passed into create_event_model

## 3.1.1 (2024-04-06)

#### Trivial

  - Fix ReadTheDocs builds. [Wesley Kendall, eda0741]

## 3.1.0 (2023-11-26)

#### Feature

  - Django 5.0 compatibility [Wesley Kendall, 934ca6d]

    Support and test against Django 5 with psycopg2 and psycopg3.

## 3.0.1 (2023-10-16)

#### Trivial

  - Add upgrading notes around the default related name changing. [Wesley Kendall, c5d8a1f]

## 3.0.0 (2023-10-16)

#### Api-Break

  - V3 release with new event trackers [Wesley Kendall, 8849fc6]

    Version three of `django-pghistory` has some of the following breaking changes:

    - Removal of code deprecated in version 2.5 related to configuring event models
    - Consolidation of the event trackers. `pghistory.Snapshot` and all custom
      event trackers such as `pghistory.BeforeDelete` and `pghistory.AfterInsertOrUpdate`
      were consolidated into three core event trackers: `pghistory.InsertEvent`,
      `pghistory.UpdateEvent`, and `pghistory.DeleteEvent`.
    - There are new default `pgh_label` values in the new event trackers
    - The `pghistory.models.Events` proxy aggregate model has some minor breaking
      functionality.

    Along with this, default arguments to `pghistory.track` were changed and
    a setting was introduced to override the global default history trackers.

    There's an entire section called "Upgrading" in the docs
    at django-pghistory.readthedocs.io that goes over the breaking changes in
    more detail, along with how to preserve the default functionality from
    version two.

#### Feature

  - Support append-only event models [Wesley Kendall, 9002d35]

    Supply `append_only=True` to `pghistory.track` or `pghistory.create_event_model` to
    create event models that protect updates and deletes.

    Set `settings.PGHISTORY_APPEND_ONLY = True` to make this the default for all event
    models.

## 2.9.0 (2023-10-09)

#### Feature

  - Add Python 3.12 support and use Mkdocs for documentation [Wesley Kendall, 4464ef3]

    Python 3.12 and Postgres 16 are supported now, along with having revamped docs using Mkdocs and the Material theme.

    Python 3.7 support was dropped.

## 2.8.0 (2023-06-08)

#### Feature

  - Added Python 3.11, Django 4.2, and Psycopg 3 support [Wesley Kendall, 647cdad]

    Adds Python 3.11, Django 4.2, and Psycopg 3 support along with tests for multiple Postgres versions.
    Drops support for Django 2.2.

## 2.7.0 (2023-04-08)

#### Feature

  - Refactory ``Snapshot`` class and add ``Changed`` condition for better extensibility. [Kevin Ramirez, 0be9242]

    Users can more easily inherit ``pghistory.Snapshot`` and use the ``pghistory.Changed``
    condition for conditional snapshots.
  - Add ``BeforeUpdateOrDelete`` tracker [Kevin Ramirez, af01e87]

    Adds a barebones ``BeforeUpdateOrDelete`` tracker for snapshotting OLD rows during an update or delete.

#### Trivial

  - Fix auto-doc formatting [madtools, de3ddf4]

## 2.6.0 (2023-03-27)

#### Bug

  - Fix documentation example for tracking events. [Zac Miller, acaaadf]
  - Fix bug when tracking context data with percent sign. [Adam Johnson, a5380fa]

    All context data is properly escaped, fixing an error that happened when
    using "%" in any context data. psycopg now escapes all context data,
    ensuring there is no SQL injection vector in the future.

#### Trivial

  - Replace usage of ``SET LOCAL`` with ``SELECT set_config`` for better pg stat reporting. [Pierre Ducroquet, ebe2d19]
  - Fix ``make lint`` command with new .gitignore changes [Kevin Ramirez, ceafe0a]
  - Fix ``PGHISTORY_OBJ_FIELD`` settings name in the docs. [Johan Van de Wauw, 2bfb23d]
  - Updated with latest django template, fixing git-tidy deployment issues [Wesley Kendall, 1a6df96]

## 2.5.1 (2022-10-12)

#### Trivial

  - Updated with latest Django template [Wesley Kendall, de8a535]
  - A safer way of determining fields when creating the snapshot triggers [Wesley Kendall, 7b368c3]

## 2.5.0 (2022-10-11)

#### Bug

  - Ignore tracking non-concrete fields [Wesley Kendall, e7b0589]

    If a field isn't concrete, pghistory no longer tries to track it.
  - Require ``django-pgtrigger>=4.5`` [Wesley Kendall, a70e0d3]

    Version 4.5 of ``django-pgtrigger`` fixes several bugs related to trigger migrations,
    especially as they relate to ``django-pghistory``.

    See the migration guide to ``django-pgtrigger`` version 4 at
    https://django-pgtrigger.readthedocs.io/en/4.5.3/upgrading.html#version-4. Upgrading
    from version 3 to 4 only affects mutli-database setups.

#### Feature

  - Automatically add the "pgh_event_model" attribute to tracked models. [Wesley Kendall, 917c396]

    When a model is tracked, a "pgh_event_model" attribute is added to the tracked model to
    make it easier to inherit the event model and access it.
  - The label argument for ``pghistory.track`` is optional [Wesley Kendall, b6a8c99]

    The label argument was previously required. Now it defaults to the name of the tracker.
  - Simplify conditions for snapshots of all fields [Wesley Kendall, e9dbc06]

    Previously when using ``pghistory.Snapshot``, the condition for the trigger would OR
    together each field to verify nothing changed. Now ``OLD.* IS DISTINCT FROM NEW.*``
    is used as the condition.
  - Restructure documentation and add more tests [Wesley Kendall, 3bc868e]

    The documemntation was overhauled for the new features and
    admin integration.
  - Added reversion capability [Wesley Kendall, c2d8b90]

    A ``revert`` method was added to event models for reverting changes.
    The method only runs if the event model tracks every field, otherwise
    a ``Runtime`` error is thrown.
  - Use ProxyField() for defining proxy columns over attributes. [Wesley Kendall, a267478]

    When inheriting the ``Events`` model or individual event models,
    one can use the ``pghistory.ProxyField`` utility to proxy
    relationships from JSON columns into structured fields. For
    example, making a foreign key for users that proxies through the
    ``user`` attribute of context.

    Previously this behavior only worked on the deprecated
    ``AggregateEvent`` model by adding additional fields. Any
    fields that are proxied must now use the ``pghistory.ProxyField``
    utility.
  - Integration with Django admin [Wesley Kendall, a9fea95]

    Installing ``pghistory.admin`` to ``settings.INSTALLED_APPS``
    will provide the following:

    * An "Events" admin page that other admins can use to display events
    * Dynamic buttons on tracked models that redirect to a pre-filtered
      events admin
    * The ability to make admins for specific event models and have them
      show up as buttons on their associated tracked model admin pages

    The default events admin has configuration parameters that can
    be set via settings.
  - New event model configuration and new aggregate ``Events`` model. [Wes Kendall, c1120f2]

    Event models can be configured with global settings
    and with overrides on a per-event-model basis.
    Previous arguments to ``pghistory.track``, such as
    ``obj_fk`` and ``context_fk`` have been deprecated
    in place of ``obj_field`` and ``context_field``.
    These new fields, along with their associated settings,
    use ``pghistory.Field`` configuration instances.

    Along with this, the ``AggregateEvent`` model has been deprecated
    in favor of the ``Events`` proxy model. The new
    ``Events`` model has similar fields and operates the same way, and
    it also has other methods for filtering aggregate events.

#### Trivial

  - Rename "tracking" module to "runtime" module. [Wesley Kendall, 43645ea]

## 2.4.2 (2022-10-06)

#### Trivial

  - Update with the latest Python template [Wesley Kendall, ef2fb6e]

## 2.4.1 (2022-09-13)

#### Trivial

  - Ensure installation of pghistory context function is installed across multiple databases [Wes Kendall, d06c758]

## 2.4.0 (2022-09-07)

#### Bug

  - Fix issues related to the ``dumpdata`` command [Wes Kendall, 8cb8036]

    Django's ``dumpdata`` command is now compatible with pghistory's AggregateEvent
    model.

## 2.3.0 (2022-09-06)

#### Bug

  - Check that "pgtrigger" is in settings.INSTALLED_APPS [Wes Kendall, fa86205]

    A check is registered with Django's check framework to verify that
    "pgtrigger" is in settings.INSTALLED_APPS when using ``django-pghistory``.

    Docs were also updated to note the requirement of pgtrigger in INSTALLED_APPS.
  - Install context tracking function in a migration [Wes Kendall, 516dc14]

    The Postgres pghistory function is now installed in a migration, alleviating
    issues that would happen when trying to migrate pghistory triggers.

## 2.2.2 (2022-09-02)

#### Trivial

  - Reference PK of user instead of ID in middleware for DRF-based flows [Wes Kendall, 2193e2b]

## 2.2.1 (2022-09-02)

#### Trivial

  - Do additional safety checks in middleware [Wes Kendall, 9678d83]

## 2.2.0 (2022-09-02)

#### Feature

  - Configure middleware tracked methods [Wes Kendall, e931757]

    Use ``settings.PGHISTORY_MIDDLEWARE_METHODS`` to configure which methods
    are tracked in the middleware. Defaults to ``("GET", "POST", "PUT", "PATCH", "DELETE")``.

## 2.1.1 (2022-08-31)

#### Trivial

  - Format trigger SQL for better compatibility with ``django-pgtrigger``>=4.5 [Wes Kendall, fa04191]

## 2.1.0 (2022-08-27)

#### Feature

  - Add setting to configure JSON encoder for context. [Zac Miller, 430225f]

    ``django-pghistory`` now uses Django's default JSON encoder
    to serialize contexts, which supports datetimes, UUIDs,
    and other fields.

    You can override the JSON encoder by setting
    ``PGHISTORY_JSON_ENCODER`` to the path of the class.

#### Trivial

  - Local development enhancements [Wes Kendall, 95a5b1d]

## 2.0.3 (2022-08-26)

#### Trivial

  - Test against Django 4.1 and other CI improvements [Wes Kendall, 953fe1d]

## 2.0.2 (2022-08-24)

#### Trivial

  - Fix ReadTheDocs builds [Wes Kendall, afbc33e]

## 2.0.1 (2022-08-20)

#### Trivial

  - Fix release note rendering and code formatting changes [Wes Kendall, 7043553]

## 2.0.0 (2022-08-08)

#### Api-Break

  - Integration with Django's migration system [Wes Kendall, e0acead]

    ``django-pghistory`` upgrades ``django-pgtrigger``, which now integrates
    with the Django migration system.

    Run ``python manage.py makemigrations`` to make migrations for the triggers
    created by ``django-pghistory`` in order to upgrade.

    If you are tracking changes to third-party models, register the tracker on
    a proxy model so that migrations are created in the proper app.

#### Feature

  - Remove dependency on ``django-pgconnection`` [Wes Kendall, aea6056]

    ``django-pghistory`` no longer requires that users wrap ``settings.DATABASES``
    with ``django-pgconnection``.

## 1.5.2 (2022-07-31)

#### Trivial

  - Updated with latest Django template, fixing doc builds [Wes Kendall, 42cbc3c]

## 1.5.1 (2022-07-31)

#### Trivial

  - Use `pk` instead of `id` to get the user's primary key [Eerik Sven Puudist, f105828]
  - Fix default_app_config warning on Django 3.2+ [Adam Johnson, 8753bc4]

## 1.5.0 (2022-05-17)

#### Feature

  - Add support for GET requests in pghistory middleware [Shivananda Sahu, ae2524e]

    Currently the middleware adds a context for POST, PUT, PATCH and DELETE requests. Updating middleware to add a context for GET requests along with POST, PUT, PATCH and DELETE.

## 1.4.0 (2022-03-13)

#### Feature

  - Allow target() to receive a queryset or list. [M Somerville, 0f34e91]

    This expands the target() function to accept a queryset or a list of
    objects on top of the existing one object.
  - Add support for delete requests in pghistory middleware [Shivananda Sahu, 322d17e]

    Currently the middleware adds a context for POST, PUT, and PATCH requests. This leaves out DELETE requests as the only ones that can affect a model without a context. Updating middleware to add a context for DELETE requests along with POST, PUT and PATCH.

#### Trivial

  - Minor code formatting fixes [Wes Kendall, d0b7664]

## 1.3.0 (2022-03-13)

#### Bug

  - Fixed bug in BeforeDelete event [Wes Kendall, aab4182]

    The BeforeDelete event was referencing the wrong trigger value (NEW).
    Code was updated to reference the proper OLD row for this event,
    and a failing test case was added.

## 1.2.2 (2022-03-13)

#### Trivial

  - Updated with latest template, dropping 3.6 support and adding Django 4 support [Wes Kendall, c160973]

## 1.2.1 (2021-05-30)

#### Trivial

  - Updated with latest python template [Wes Kendall, 09f6cfb]

## 1.2.0 (2020-10-23)

#### Feature

  - Upgrade pgtrigger and test against Django 3.1 [Wes Kendall, 176fb13]

    Uses the latest version of django-pgtrigger. Also tests against Django 3.1
    and fixes a few bugs related to internal changes in the Django codebase.

## 1.1.0 (2020-08-04)

#### Bug

  - Escape single quotes in tracked context [Wes Kendall, 40f758e]

    Invalid SQL was generated from context values with single quotes when
    using ``pghistory.context``. Single quotes are now properly escaped, and
    a failing test case was created to cover this scenario.

## 1.0.1 (2020-06-29)

#### Trivial

  - Updated with the latest public django app template. [Wes Kendall, fc1f3e4]

## 1.0.0 (2020-06-27)

#### Api-Break

  - Initial release of django-pghistory. [Wes Kendall, ecfcf96]

    ``django-pghistory`` provides automated and customizable history
    tracking for Django models using
    [Postgres triggers](https://www.postgresql.org/docs/12/sql-createtrigger.html).
    Users can configure a number of event trackers to snapshot every model
    change or to fire specific events when certain changes occur in the database.

    In contrast with other Django auditing and history tracking apps
    (seen [here](https://djangopackages.org/grids/g/model-audit/)),
    ``django-pghistory`` has the following advantages:

    1. No instrumentation of model and queryset methods in order to properly
       track history. After configuring your model, events will be tracked
       automatically with no other changes to code. In contrast with
       apps like
       [django-reversion](https://django-reversion.readthedocs.io/en/stable/),
       it is impossible for code to accidentally bypass history tracking, and users
       do not have to use a specific model/queryset interface to ensure history
       is correctly tracked.
    2. Bulk updates and all other modifications to the database that do not fire
       Django signals will still be properly tracked.
    3. Historical event modeling is completely controlled by the user and kept
       in sync with models being tracked. There are no cumbersome generic foreign
       keys and little dependence on unstructured JSON fields for tracking changes,
       making it easier to use the historical events in your application (and
       in a performant manner).
    4. Changes to multiple objects in a request (or any level of granularity)
       can be grouped together under the same context. Although history tracking
       happens in Postgres triggers, application code can still attach metadata
       to historical events, such as the URL of the request, leading to a more
       clear and useful audit trail.
