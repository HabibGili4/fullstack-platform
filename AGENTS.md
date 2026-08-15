# AGENTS.md — latihan-fastapi

## Ringkasan
FastAPI learning project (modular). Bukan production-ready. Entry point: `app.main:app`.

## Perintah cepat (yang berguna)
- Install: `uv sync`
- Setup env: `cp .env.example .env`
- Run dev: `uv run uvicorn app.main:app --reload`
- Migrate DB (PostgreSQL): `alembic upgrade head`
- Seed accounts (opsional): `python seed_accounts.py`
- Seed test users (RBAC): `python seed_roles.py`
- Run tests: `uv run pytest tests/ -v`
- Run tests + coverage: `uv run pytest tests/ --cov=app --cov-report=term-missing`
- Docker compose: `docker compose up --build -d`
- Docker stop: `docker compose down`
- Docker stop + hapus data: `docker compose down -v`

## Struktur & alur
- Modular route: `app/api/{accounts,health,posts,products,tasks,users}.py`
- Core: `app/core/config.py` (pydantic-settings), `app/core/database.py` (engine + `get_db`), `app/core/permissions.py` (RBAC), `app/core/logging.py` (setup_logging), `app/core/ports.py` (interfaces)
- Auth: `app/dependencies/auth.py:get_current_user` (JWT Bearer, bukan mock)
- DI factories: `app/dependencies/services.py` (get_*_service)
- Permission check: `app/dependencies/permissions.py:require_permission`
- Service/Repository pattern di `app/services/*` dan `app/repositories/*`
- Models: `app/models/*` (SQLAlchemy mapped columns) — User, Post, Product, Task, Account, RefreshToken
- DB auto-create saat startup via `Base.metadata.create_all` di lifespan (`app/main.py`)

## Autentikasi (JWT)
- Login: `POST /api/v1/users/login` → body `{"email": "...", "password": "..."}` → returns `{"access_token": "...", "refresh_token": "...", "token_type": "bearer"}`
- Refresh: `POST /api/v1/users/refresh` → body `{"refresh_token": "..."}` → returns token baru + refresh token baru
- Akses endpoint terproteksi: header `Authorization: Bearer <token>`
- GET current user: `GET /api/v1/users/me` → returns data user dari token
- Password hashing: bcrypt via `passlib` (`app/services/auth_service.py` + `app/services/password_hasher.py`)
- JWT encode/decode: `python-jose` dengan `HS256` + `SECRET_KEY`
- Token expiry: access 30 menit, refresh 7 hari (configurable)
- Refresh token rotation: setiap refresh, token lama di-revoke (single-use)
- Login baru revoke semua refresh token lama (logout semua device)
- Behavior:
  | Request | Hasil |
  |---------|-------|
  | Tanpa token | 401 |
  | Token salah | 401 |
  | Token expired | 401 |
  | Token valid | 200 + data user |
  | Refresh token valid | 200 + token baru |
  | Refresh token expired/sudah dipakai | 401 |

## Authorization (RBAC)
- Role: `admin`, `manager`, `editor`, `user` (default: `user`)
- Permissions didefinisikan di `app/core/permissions.py`
- Cek permission: `require_permission("product:read")` dependency
- Products endpoint:
  | Endpoint | Method | Permission | Admin | Editor | User |
  |----------|--------|------------|-------|--------|------|
  | `/products` | GET | `product:read` | ✓ | ✓ | ✓ |
  | `/products` | POST | `product:create` | ✓ | ✓ | ✗ |
  | `/products/{id}` | PUT | `product:update` | ✓ | ✓ | ✗ |
  | `/products/{id}` | DELETE | `product:delete` | ✓ | ✗ | ✗ |
- Tasks endpoint:
  | Endpoint | Method | Permission | Admin | Manager | Editor | User |
  |----------|--------|------------|-------|---------|--------|------|
  | `/tasks` | GET | `task:view` | ✓ | ✓ | ✗ | ✗ |
  | `/tasks` | POST | `task:create` | ✓ | ✓ | ✗ | ✗ |
  | `/tasks/{id}` | PUT | `task:update` | ✓ | ✓ | ✗ | ✗ |
  | `/tasks/{id}` | DELETE | `task:delete` | ✓ | ✗ | ✗ | ✗ |
- Role di JWT payload (bukan DB lookup) → user harus login ulang jika role berubah
- Seed test users: `python seed_roles.py`

## Docker
- Dockerfile: `python:3.11-slim` + `uv`, port `8001`
- docker-compose.yml: 2 services (`app` + `db`)
- Port mapping: app=8001, db=5433 (PostgreSQL)
- Env strategy: `env_file: .env` + `environment:` override (hanya DATABASE_URL hostname)
- DB: PostgreSQL 16 Alpine, DB name `engineering_playbook`, healthcheck included
- Persistent volume: `db_data`
- Run: `docker compose up --build -d`
- Logs: `docker compose logs -f app`
- Akses DB dari host: `psql -h localhost -p 5433 -U postgres -d engineering_playbook`

## Testing
- Framework: `pytest` + `httpx` + `pytest-cov`
- 64 tests, 85% coverage
- Struktur:
  - `tests/unit/services/` — service tests (mock dependencies)
  - `tests/unit/repositories/` — repository tests (real DB)
  - `tests/integration/api/` — API endpoint tests (real DB)
  - `tests/integration/database/` — DB connection tests
  - `tests/e2e/` — end-to-end flow tests
  - `tests/test_security_matrix.py` — auth & RBAC edge cases
- Jalankan: `uv run pytest tests/ -v`
- Coverage: `uv run pytest tests/ --cov=app --cov-report=term-missing`

## Penting (sering salah duga)
- `get_current_user` pakai JWT Bearer (bukan mock). Token di-decode via `python-jose`, user di-lookup dari DB.
- Password hashing: bcrypt via `passlib` (`app/services/password_hasher.py`). Bukan SHA-256/hashlib.
- `alembic.ini` sqlalchemy.url di-override dari `settings.DATABASE_URL` di `alembic/env.py`.
- `docker-compose.yml` pakai `env_file: .env` + `environment:` override. Hanya `DATABASE_URL` yang di-override (hostname `db` vs `localhost`).
- Role di JWT payload, bukan DB lookup → login ulang jika role berubah.
- Products punya ownership check: editor hanya bisa update/delete product milik sendiri.

## File kunci
- `app/main.py` — entry point + lifespan
- `app/dependencies/auth.py` — get_current_user (JWT Bearer)
- `app/dependencies/services.py` — DI factories
- `app/dependencies/permissions.py` — require_permission
- `app/core/config.py` — Settings (pydantic-settings)
- `app/core/database.py` — engine + get_db
- `app/core/permissions.py` — ROLE_PERMISSIONS
- `app/core/ports.py` — interfaces (IPasswordHasher, ITokenService)
- `app/services/auth_service.py` — authenticate + refresh
- `app/services/user_service.py` — CRUD users
- `app/services/product_service.py` — CRUD products + ownership check
- `app/repositories/user_repository.py` — DB operations
- `alembic.ini`, `alembic/env.py` — migrations
- `Dockerfile` — container build
- `docker-compose.yml` — orchestration
- `tests/conftest.py` — test fixtures
- `seed_accounts.py`, `seed_roles.py` — seed data

## Opsional: verifikasi singkat
Kalau mengubah flow auth, pastikan endpoint depend `get_current_user` masih bisa diakses (contoh: `GET /api/v1/users/`). Jalankan `uv run pytest tests/ -v` untuk memastikan tidak ada regression.
