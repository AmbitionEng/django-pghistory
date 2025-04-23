# Performance and Scaling

Here we overview some of the main things to consider regarding performance and scale. It's useful to consider some of these recommendations before using `django-pghistory` because some changes can involve tricky migrations if done after the fact.

## Trigger Execution

[Postgres row-level triggers](https://www.postgresql.org/docs/current/sql-createtrigger.html) are used by default to store events. When using a [pghistory.InsertEvent][] tracker, for example, this means a snapshot of your model is saved every time it is inserted or updated. In other words, `Model.objects.bulk_create` or `Model.objects.update` can create multiple additional event rows across multiple queries.

!!! note

    While this will have a performance impact when creating or updating models, keep in mind that triggers run in the database and do not require expensive round trips from the application.

One can override this behavior by using [statement-level triggers](https://www.geeksforgeeks.org/plsql-statement-level-triggers/), meaning history triggers will run per statement instead of per row. This can substantially speed-up large bulk operations where history triggers are fired.

This can be enabled in the following hierarchy:

- On the individual tracker level:
```python
@pghistory.track(pghistory.InsertEvent(level=pghistory.Statement))
...
```
- On an event model:
```python
@pghistory.track(level=pghistory.Statement)
...
```
- Globally in settings:
```python
PGHISTORY_LEVEL = pghistory.Statement
```

In other words, settings from the bottom of the hierarchy (e.g. settings) do not override any explicit setting of the level at higher levels.

!!! danger

    When using statement-level history triggers, conditions that span old and new rows, such as [pghistory.AnyChange][], do **not** track changes if the primary key is updated. If your application commonly updates primary keys, avoid using statement-level triggers.

We recommend using statement-level triggers for performance-critical areas of your application, especially when the common use case is large bulk inserts or updates. Statement-level triggers generally underperform their row-level counterparts when only operating on small amounts of rows at a time, although the difference should be negligible.

## Context Tracking

### Ignoring Context

When [tracking application context](./context.md), context will be updated or inserted into the main `Context` model's table for each trigger invocation.

If context is not important to some of your event tables, you can turn it off entirely:

- On an event model:
```python
@pghistory.track(context_field=None)
...
```
- Globally in settings:
```python
PGHISTORY_CONTEXT_FIELD = None
```

!!! note

    As with other settings, these provide the default values. More granular settings will not be overridden by the defaults.

When setting the context field to `None`, the event model(s) won't include the `pgh_context` field, and the associated context operations won't happen when those event triggers fire. This can be a performance improvement for those triggers while letting other historical events be linked with context.

### Denormalizing Context

As discussed in the [Denormalizing Context](event_models.md#denormalizing_context) section, you can avoid doing an update or insert on the main context table and instead duplicate the context data on the event model. This not only reduces the overhead of maintaining an index to the context table from the event table, but it also reduces the contention on a shared context table among multiple event triggers.

Large amounts of events should also be taken into consideration too. As the context table grows, so will the indices and the associated time it takes to update the index. Denormalizing context reduces the overhead at the expense of more storage. It also makes it easier to partition your event tables.

## Indices and Foreign Key Constraints

By default, all event tables use unconstrained foreign keys. Event tables also drop all indices except for foreign keys.

If you don't plan to query or join your event models, you may not need to index the foreign keys. You could instead set the default foreign key behavior to:

```python
PGHISTORY_FOREIGN_KEY_FIELD = pghistory.ForeignKey(db_index=False)
```

Keep in mind that this could negatively impact the performance of the admin integration. If you want to continue using core admin functionality, be sure to index the object field, otherwise the foreign key settings will override it:

```python
PGHISTORY_OBJ_FIELD = pghistory.ObjForeignKey(db_index=True)
```

If you prefer that your foreign keys have referential integrity, do:

```python
PGHISTORY_FOREIGN_KEY_FIELD = pghistory.ForeignKey(
    db_constraint=True,
    on_delete=pghistory.DEFAULT
)
```

Remember that there will be a performance hit for maintaining the foreign key constraint, and Django will also have to cascade delete more models.

## The `Events` Proxy Model

The [pghistory.models.Events][] proxy model uses a common table expression (CTE) across event tables to query an aggregate view of data. Postgres 12 optimizes filters on CTEs, but you may experience performance issues if trying to directly filter `Events` on earlier versions of Postgres. Similarly, aggregating many large event tables is likely to simply just be slow given the nature of this query.

See [Aggregating Events and Diffs](aggregating_events.md) for more information on how to use the special model manager methods to more efficiently filter events.
