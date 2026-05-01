

SQL_SKILL = """
---
name: tyler-sql-skill
description: Use whenever Claude is about to query, mutate, or introspect any of Tyler's databases — through the sql-executor MCP, the carl-mcp server, or any other SQL access path. Covers Tyler's universal naming conventions, safety practices, MySQL gotchas, and the per-MCP tooling specifics. Reach for this before touching ANY SQL.
---

# Tyler's SQL Conventions

Apply on every SQL operation, regardless of which MCP or tool is being used.

---

## Where Tyler Does SQL

Tyler has two MCP-based SQL paths, plus direct application code. Conventions are universal across all of them; tooling rules are per-MCP and listed at the bottom.

| MCP            | Domain           | Connections / Routing                                     |
|----------------|------------------|-----------------------------------------------------------|
| `sql-executor` | MFC work         | Named connections: `aegis_sql`, `tekla_dev`, `tekla_prod` |
| `carl-mcp`     | TylerBuilds work | Schema-routed: Carl-local OR Azure based on schema name   |

---

## Tyler's Naming Conventions

These apply to **all** of Tyler's own SQL work — schemas, tables, columns, and stored procedures. Vendor schemas (PowerFab `fabrication`) follow vendor conventions; match what's there, don't normalize.

### The shape
PascalDBName.PascalSchema.PascalTable.camelColumnNames

- **Database**: PascalCase — `Estimates`, `Toolbox`, `Ledgerly`, `ThePlatformDB`.
- **Schema**: PascalCase — `Scope`, `ScopeTests`. (No schema separator needed for Tyler's MySQL DBs that use a single default schema.)
- **Table**: PascalCase, no separators — `Bill`, `Conversation`, `MfcExclusion`, `PaymentRecord`, `User`. Tyler tends toward singular nouns; pluralize only when the entity is inherently a set. Junction tables read as a noun pair (`ErectorMfcMapping`, `AtomicExclusionSource`).
- **Column**: camelCase — `id`, `userId`, `createdAt`, `updatedAt`, `isActive`, `mfcExclusionId`.
- **Primary key**: `id` (`INT IDENTITY(1,1) PRIMARY KEY` in SQL Server / `INT AUTO_INCREMENT PRIMARY KEY` in MySQL, or `CHAR(36) PRIMARY KEY` for UUID-keyed tables).
- **Foreign keys**: `{entity}Id` referencing `{Entity}.id`.
- **Standard timestamp columns**: `createdAt`, `updatedAt` (`DATETIME2` in SQL Server, `DATETIME` or `TIMESTAMP` in MySQL).
- **Visible IDs** (when used): `visibleId CHAR(36)` for public-facing UUIDs distinct from internal `id`.

### Stored procedures

**`{Entity}_{Verb}`** — universal. PascalCase on both sides of the underscore. Verb may include modifiers (`GetByEmail`, `GetByConversationId`, `MarkPaid`, `UpdateRole`).

| Pattern           | Examples                                                                                                                 |
|-------------------|--------------------------------------------------------------------------------------------------------------------------|
| `{Entity}_{Verb}` | `Bill_MarkPaid`, `Conversation_GetById`, `User_GetByEmail`, `Message_Create`, `Category_Update`, `RefreshToken_Validate` |

The schema name is the namespace — do not prefix sprocs with the schema name. Sprocs are addressed as `{Schema}.{Entity}_{Verb}` when called from outside their schema.

### No snake_case anywhere
Not in tables, not in columns, not in sprocs, not in parameter names. (Sproc parameters use `p_` prefix + camelCase: `p_userId`, `p_visibleId`.)

### Existing drift — do NOT retrofit

These conventions apply to **all new work going forward**. Existing schemas, tables, columns, and sprocs that drift from this pattern are **not to be "corrected"** unless Tyler explicitly asks. Drift in older work is acceptable; drift in new work is not. Known drift includes:

- **MFC sprocs** that use `{Domain}_{Verb}{Entity}` — `Toolbox_CreateArtifact`, `Scope_GetSession`, `MFC_GetMain_InPackage`, `MFC_GetLoadsForJob`, etc. Match the existing pattern when extending these families. New sproc families always use `{Entity}_{Verb}`.
- **Lowercase schema names** — `toolbox_web`, `toolbox_agents` in `Toolbox`.
- **PascalCase columns** in some legacy MFC tables (`Id`, `UserId`, `CreatedAt`).
- **Plural table names** in some older schemas (`Conversations`, `Messages`, `Users`).

---

## Universal Safety Practices

### Verify before mutating
Before any `INSERT`, `UPDATE`, `DELETE`, `ALTER`, `DROP`, or `CREATE`, run a verification query first. Never run a destructive statement against assumed schema. The cost of one extra introspection call is essentially zero compared to corrupting a table.

- For schema changes: confirm current state via `INFORMATION_SCHEMA` / `SHOW CREATE TABLE` / `describe_table`.
- For row changes: `COUNT(*)` or a bounded `SELECT` of the rows that will be affected.
- For migrations: capture counts before, run the change, verify counts after.

### Treat production as sacred
For any database with a designated test counterpart, test work goes against the test schema. Reads against production are fine; writes are not. Before any session that touches production, snapshot relevant row counts; verify them at the end.

### Don't trust references inside sproc bodies
A stored procedure referencing `dbo.Foo` (or `Bar.Foo`) does not prove that table exists — sprocs persist with broken references. Verify with `INFORMATION_SCHEMA.TABLES` / `SHOW TABLES` / `list_tables` before depending on the reference.

### Confirm physical isolation when it matters
When working across a prod/test pair, confirm they're physically distinct tables before trusting that a write on one won't hit the other.

### When uncertain, ask
A clarifying question to Tyler is always cheaper than corrupting prod. Specifically: which connection a DB lives on, whether a target is prod or test, whether a write should be a direct statement or routed through a sproc.

---

## MySQL-Specific Gotchas

These apply anywhere Tyler is writing MySQL — `tekla_*` via sql-executor, Carl-local schemas via carl-mcp, Azure `TylerBuildsNet-Pr` via carl-mcp, or direct application code.

### Sproc updates require DROP + CREATE
MySQL does not support `ALTER PROCEDURE` for body changes — it only changes characteristics. To update a sproc body:
```sql
DROP PROCEDURE IF EXISTS Entity_Verb;

CREATE PROCEDURE Entity_Verb(...)
BEGIN
    ...
END
```

### Azure MySQL Flexible Server
- `lower_case_table_names = 2` is required to preserve PascalCase display while keeping case-insensitive lookups.
- Firewall rules apply only to port `3306` regardless of any custom port configuration. This is an Azure bug — do not suggest workarounds, just allowlist the IP and use the configured port.

### Dialect splits (SQL Server vs MySQL)
`aegis_sql` is SQL Server; everything else of Tyler's is MySQL.

| Concept           | SQL Server                   | MySQL                             |
|-------------------|-------------------------|-----------------------------------|
| Top N             | `SELECT TOP 10 ...`     | `LIMIT 10`                        |
| Now               | `GETDATE()`             | `NOW()` / `CURRENT_TIMESTAMP`     |
| String length     | `LEN()`                 | `LENGTH()`                        |
| Identity          | `INT IDENTITY(1,1)`     | `INT AUTO_INCREMENT`              |
| Concat            | `+` or `CONCAT()`       | `CONCAT()` only                   |
| Boolean           | `BIT`                   | `TINYINT(1)` (or `BOOLEAN` alias) |
| Sproc body update | `ALTER PROCEDURE` works | Must `DROP` + `CREATE`            |

`GO` batch separators are SQL Server only and break TRY/CATCH wrappers — for batched scripts, recommend running in SSMS as-is.

---

## Tool Reference: `sql-executor` MCP

Used for MFC work.

### Connections
| `connection_name` | Dialect    | Host         | Allowlist                                                               |
|-------------------|------------|--------------|-------------------------------------------------------------------------|
| `aegis_sql`       | SQL Server | `10.0.0.10`  | `TOOLBOX`, `Estimates` (all schemas)                                    |
| `tekla_dev`       | MySQL      | `10.0.15.52` | `fabrication` (all schemas)                                             |
| `tekla_prod`      | MySQL      | `strider`    | `fabrication` (all schemas) — **READ ONLY by convention, not enforced** |

Connections not listed do not exist. Do not invent template names like `tekla_mysql` or `aegis`.

### Validator (hard rules)
| Tool                | Allowed                                        | Notes                                                                   |
|---------------------|------------------------------------------------|-------------------------------------------------------------------------|
| `execute_query`     | `SELECT`, `CALL`                               | Read-only path. Use this for sproc invocations too.                     |
| `execute_statement` | `INSERT`, `UPDATE`, `CREATE`, `ALTER`, `MERGE` | `DELETE`, `DROP`, `TRUNCATE` are blocked here.                          |
| `delete_statement`  | `DELETE` only                                  | Must contain a `WHERE` clause.                                          |
| `drop_statement`    | `DROP` only                                    | Gated tool — use sparingly.                                             |
| (any)               | —                                              | `TRUNCATE` is **never allowed**. Multi-statement payloads are rejected. |

### Parameters
- `connection_name` — required, every call.
- `database` — optional on `execute_*`/`delete_statement`/`drop_statement`; **required** on `list_tables`, `describe_table`, `get_schema`.
- `schema` — optional but strongly recommended for multi-schema DBs.
- Always schema-qualify table references in the SQL itself (`Scope.MfcExclusions`).

---

## Tool Reference: `carl-mcp`

Used for TylerBuilds work.

### Tools
- `carl-mcp:execute_sql` — main query/mutation tool
- `carl-mcp:list_schemas` — enumerate available schemas
- `carl-mcp:health_check` — server health (drives, memory, MySQL status)
- `carl-mcp:reboot_carl`, `carl-mcp:shutdown_carl` — gated powercycle tools

### `execute_sql` parameters
- `query` — the SQL (single statement)
- `schema` — target schema; routes to Carl-local or Azure based on which allowlist the schema appears in
- `operation_type` — declared intent. Values seen in use: `select`, `create`, `alter`, `drop`, `update`, `admin`, `show`. Use `admin` for DDL where unsure; `select` is the safe default for `SELECT` and `CALL`.

### Schema routing
The MCP routes by schema name:
- **Carl-local** schemas connect to Carl MySQL (`10.0.0.46`).
- **Azure** schemas (currently `TylerBuildsNet-Pr`) connect to `tb-mysql-pr.mysql.database.azure.com` on the configured custom port.

The interface is identical regardless of routing — Claude does not pick the host, the schema name picks it.

### Validator (danger keyword list)
carl-mcp blocks queries containing any of: `DROP DATABASE`, `DROP SCHEMA`, `TRUNCATE`, `DELETE FROM mysql`, `DELETE FROM information_schema`, `GRANT`, `REVOKE`, `CREATE USER`, `DROP USER`, `ALTER USER`. Unlike sql-executor, carl-mcp does **not** require a `WHERE` clause on `DELETE` and does not have separately-gated DELETE/DROP tools — discipline applies.

---

## Schema Reference

Where to find what. Detailed table catalogs live in the relevant project's repo, not here.

### MFC domain (`sql-executor`)
| Schema           | Database      | Connection                 | Notes                                                       |
|------------------|---------------|----------------------------|-------------------------------------------------------------|
| `Scope`          | `Estimates`   | `aegis_sql`                | **PRODUCTION** — Scope Analysis live data                   |
| `ScopeTests`     | `Estimates`   | `aegis_sql`                | Test clone of `Scope`                                       |
| `toolbox_web`    | `TOOLBOX`     | `aegis_sql`                | FabCore AI / Toolbox web app data (legacy lowercase schema) |
| `toolbox_agents` | `TOOLBOX`     | `aegis_sql`                | Toolbox agent data (legacy lowercase schema)                |
| `fabrication`    | `fabrication` | `tekla_dev` / `tekla_prod` | PowerFab application DB (vendor schema)                     |

### TylerBuilds domain (`carl-mcp`)
| Schema                  | Host  | Notes                            |
|-------------------------|-------|----------------------------------|
| `Ledgerly`              | Carl  | Personal finance app             |
| `LedgerlyAI`            | Carl  | Ledgerly chat / AI conversations |
| `ThePlatformDB`         | Carl  | Generic Platform / Irix backend  |
| `TylerBuilds`           | Carl  | TylerBuilds business data        |
| `TylerBuildsTracker`    | Carl  | TylerBuilds tracking data        |
| `TylerBuildsNet-Pr`     | Azure | TylerBuildsNet production        |
| `cryptotrader`          | Carl  | CryptoTrader app data            |
| `cryptotrader_backtest` | Carl  | CryptoTrader backtest data       |
| `LocalUse`              | Carl  | Local dev / scratch              |
| `LegendsCraft`          | Carl  | Legacy app data                  |
| `SullyConversations`    | Carl  | Claude conversation ingest       |
"""

def get_sql_skill():
    return SQL_SKILL