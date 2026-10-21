# ADR-003: shared owner foundation and first local C1 adapter

20 October 2026. Status: implemented in source, unqualified. Input: architecture branch `0fd018e60373ca08551ebd7d57ac859dbc8b64fd`. User authorized shared foundation followed by Observation, retaining the structure-first/no-qualification direction.

The eight owners remain one Python package with typed value contracts and dependency ports. C0 composes the application; C1 alone owns observation storage. C2-C7 declare their functions and explicitly raise unavailable. The current master, nine representation families and 28-pair/56-lane design remain unchanged.

Use a bounded SQLite implementation for the first local recording path. The earlier observation plan explicitly offered SQLite as a local candidate. The later tool reference prefers Postgres/SQLAlchemy and an artifact store for the larger ecosystem. This decision narrows the first adapter, rather than silently installing that larger topology. Postgres remains a later implementation choice behind ObservationStore; its adapter/migrations and compatibility qualification are unimplemented.

Payload chunks are SQLite BLOB rows committed with the observation, manifest, retry identity and notification/log position in the SAME transaction. Unlike a separate payload directory, this requires no cross-store acknowledgement protocol. No global content deduplication is needed to preserve correct occurrence identity. The observation log also serves as the durable replay/outbox source; it is not duplicated into an unsynchronized notification table.

This trades write concurrency and large-object storage efficiency for a smaller, explicit atomicity boundary. One DB per workspace, one serialized writer, finite objects, no distributed ingestion or HA. Large live streams must be segmented upstream with explicit sequence/completeness profiles; native packet/chunk boundaries belong in the opaque profiles if needed. Database storage chunks do not imply source packet boundaries. A future external artifact backend must implement the staged-object durability/reconciliation protocol before it can acknowledge its own durability class.

Binding: Python source supports 3.12-3.14; development host is Python 3.14.0, SQLite 3.50.4 and Pydantic 2.12.5. Pydantic is pinned as the only runtime third-party dependency. No package installation or binary lockfile generation occurred. SQLite is provided by Python and its exact binary is not vendored. Setuptools is only the bounded build backend; reproducible release locking remains open. No vLLM, student/teacher checkpoint, mathematical backend, broker, HTTP server or infrastructure is installed by this increment.

Sources consulted for API semantics: [Python sqlite3](https://docs.python.org/3.14/library/sqlite3.html), [SQLite transactions](https://www.sqlite.org/lang_transaction.html), [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/). They support the API choices, not a durability/performance claim for this hardware.

See [runtime specification](../implementation/FOUNDATION_C1_RUNTIME.md) for requirement allocation, interfaces, failure semantics, limits and open gates. The local FULL acknowledgement is explicitly labelled unqualified. Source review, syntax parsing and imports are not product qualification.
