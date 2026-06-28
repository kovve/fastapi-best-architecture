# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development lifecycle

```bash
# Automated first-time setup (creates .env, installs deps, creates DB, runs init SQL)
uv run fba init --auto

# Interactive re-initialization (recreate tables + seed data)
uv run fba init

# Start API server (Granian ASGI, dev mode with hot-reload)
uv run fba run                    # defaults to 127.0.0.1:8000
uv run fba run --host 0.0.0.0 --port 8080
uv run fba run --workers 4 --no-reload   # multi-worker (production)

# Format and lint
uv run fba format                 # runs prek (ruff check --fix + ruff format)

# Sync project + plugin dependencies
uv run fba deps                   # sync uv.lock + install all plugin deps
uv run fba deps --no-project      # only plugin deps
uv run fba deps --no-plugin       # only project deps
uv run fba deps --plugin dict     # sync deps for specific plugin
```

### Testing

```bash
# Run all tests
uv run pytest

# Run a single test file
uv run pytest backend/app/admin/tests/api_v1/test_auth.py

# Run with verbose output
uv run pytest -v

# Run a specific test function
uv run pytest backend/app/admin/tests/api_v1/test_auth.py::test_login
```

### Database migrations (Alembic)

```bash
uv run fba alembic revision              # autogenerate migration
uv run fba alembic revision -m "desc"    # with custom message
uv run fba alembic upgrade               # to head
uv run fba alembic upgrade <revision>    # to specific version
uv run fba alembic downgrade             # back one version
uv run fba alembic current -v            # show current revision
uv run fba alembic history               # show migration history
```

### Plugins

```bash
uv run fba add --repo-url <git-url>         # install plugin from git
uv run fba add --path <zip-path>            # install plugin from local zip
uv run fba add --repo-url <url> -f          # install frontend plugin
uv run fba remove                           # interactive uninstall
uv run fba remove --plugin <name>           # uninstall specific plugin
```

### Celery task queue

```bash
uv run fba celery worker -l debug           # start worker (gevent pool)
uv run fba celery beat -l debug             # start beat scheduler
uv run fba celery flower                    # start flower monitor (port 8555)
```

### Code generation

```bash
uv run fba import --app <app_name> --tn <table_name>   # import table metadata
uv run fba codegen                                     # interactive generate
uv run fba codegen -p                                  # preview only, no file writes
```

### Execute arbitrary SQL

```bash
uv run fba --sql /path/to/script.sql     # run SQL script in a transaction
```

### Docker

```bash
docker compose up -d                     # start all services
docker compose build --build-arg SERVER_TYPE=fba_server
```

## Architecture

### Three-tier design

Every business domain (`backend/app/admin/`, `backend/app/task/`, and each plugin) follows a strict layered structure:

| Layer          | Directory        | Role                                         |
|----------------|------------------|----------------------------------------------|
| API (view)     | `api/`           | Route handlers, request/response processing  |
| Schema (DTO)   | `schema/`        | Pydantic models for request/response validation |
| Service        | `service/`       | Business logic, orchestration                |
| CRUD (DAO)     | `crud/`          | Database access via `sqlalchemy-crud-plus`   |
| Model          | `model/`         | SQLAlchemy ORM models                        |

### Model inheritance hierarchy (see `backend/common/model.py`)

- **`MappedBase`** — the root declarative base (`AsyncAttrs + DeclarativeBase`). Auto-generates `__tablename__` from the class name.
- **`DataClassBase`** — `MappedAsDataclass + MappedBase`, abstract. Use for models that don't need the standard timestamp/delete columns.
- **`Base`** — `DataClassBase + DateTimeMixin + LogicalDeleteMixin`. The most common base — provides `created_time`, `updated_time`, `deleted`, `deleted_time`.
- **`UserMixin`** — provides `created_by` / `updated_by`.
- **`id_key`** — a reusable `Annotated` primary key type that respects `DATABASE_PK_MODE` (autoincrement vs snowflake).

### Application lifecycle (`backend/main.py` → `backend/core/registrar.py`)

1. `main.py` checks required plugins and installs plugin dependencies at import time
2. `register_app()` creates the FastAPI instance and wires everything up
3. The `lifespan` (startup) initializes: DB tables → Redis → Snowflake (optional) → OperaLog consumer → cache Pub/Sub listener
4. On shutdown: Pub/Sub stopped, OperaLog task cancelled, Snowflake released, Redis closed

### Middleware stack (order matters, applied bottom-up in code)

1. **CORS** — configurable origins, credentials support
2. **ContextVar** — request ID (OpenTelemetry trace ID when Grafana enabled, otherwise UUID)
3. **AccessMiddleware** — access logging
4. **I18nMiddleware** — internationalization (default `zh-CN`)
5. **JwtAuthMiddleware** — Starlette `AuthenticationBackend`; extracts Bearer token, validates via Redis, sets `request.user`
6. **StateMiddleware** — request-scoped state
7. **OperaLogMiddleware** — async queued operation logging

### Authentication & authorization

- JWT tokens stored in Redis (not stateless); access + refresh token pairs
- `jwt_authentication()` validates token → Redis lookup → loads user from DB/cache → `GetUserInfoWithRelationDetail`
- RBAC supports two modes via `RBAC_ROLE_MENU_MODE`:
  - **Role-menu mode** (default): permissions derived from menu `perms` field on user's enabled roles
  - **Casbin mode**: delegates to the `casbin_rbac` plugin
- `DependsJwtAuth` / `DependsRBAC` / `DependsSuperUser` are the dependency injection points

### Plugin system (`backend/plugin/`)

Two plugin types defined in each plugin's `plugin.toml`:
- **App-level** (`routers`): injects new top-level routes into the main router. Uses `api/router.py` as entry point.
- **Extend-level** (`api`): injects routes into an existing app's router (e.g., extending `admin`). The plugin's API files are merged into the target app's API layer.

Plugin lifecycle: config validated → dependencies installed → SQL scripts executed → models imported → routes injected. Required plugins (listed in `PLUGIN_REQUIRED`) cannot be removed.

### Key technology choices

- **Server**: Granian (Rust-based ASGI) instead of Uvicorn — better performance, native reload filtering
- **Package management**: uv with lockfile (`uv.lock`), custom PyPI mirror (aliyun)
- **Serialization**: `msgspec` for JSON responses (`MsgSpecJSONResponse`) — faster than stdlib json
- **Async pool**: `celery-aio-pool` for Celery workers to support async tasks with `gevent`
- **ORM extras**: `sqlalchemy-crud-plus` for declarative CRUD base classes
- **Pagination**: `fastapi-pagination` with SQLAlchemy async support
- **Caching**: Two-tier — in-process LRU (`cachebox`) + Redis. Pub/Sub-based cross-instance invalidation.
- **Rate limiting**: `pyrate-limiter` backed by Redis
- **i18n**: Custom middleware with locale files in `backend/locale/`

### Configuration (`backend/core/conf.py`)

Uses `pydantic-settings` with a custom source priority: env vars → `.env` file → plugin `plugin.toml` settings. `ENVIRONMENT=prod` triggers production-only defaults: OpenAPI docs hidden, Celery switched to RabbitMQ, Grafana metrics enabled.

### Database compatibility

Supports both MySQL (`asyncmy`) and PostgreSQL (`asyncpg`). Compatibility is handled via:
- `UniversalText` type decorator (LONGTEXT vs TEXT)
- `TimeZone` type decorator (timezone-aware datetime)
- Separate SQL script directories (`backend/sql/mysql/`, `backend/sql/postgresql/`)
- `DataBaseType` enum used throughout for conditional logic

### Testing setup (`backend/conftest.py`)

- `TestClient` from Starlette (not httpx) with overridden DB dependencies
- Test DB uses `{DATABASE_SCHEMA}_test` naming
- `token_headers` fixture logs in as `admin / 123456` for authenticated test requests
- Tests live alongside the domain code (e.g., `backend/app/admin/tests/`)
