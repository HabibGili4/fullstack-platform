# AGENTS.md — latihan-fastapi

## Ringkasan
FastAPI learning project (modular). Bukan production-ready. Entry point: `app.main:app`.

## Perintah cepat (yang berguna)
- Install: `uv sync`
- Setup env: `cp .env.example .env`
- Run dev: `uv run uvicorn app.main:app --reload`
- Migrate DB (PostgreSQL): `alembic upgrade head`
- Seed accounts (opsional): `python seed_accounts.py`

## Struktur & alur
- Modular route: `app/api/{accounts,health,posts,products,users}.py`
- Core: `app/core/config.py` (pydantic-settings), `app/core/database.py` (engine + `get_db`)
- Auth mock: `app/dependencies.py:get_current_user` (hardcoded user, belum JWT/OAuth)
- Service/Repository pattern di `app/services/*` dan `app/repositories/*`
- Models: `app/models/*` (SQLAlchemy mapped columns)
- DB auto-create saat startup via `Base.metadata.create_all` di lifespan (`app/main.py`)

## Autentikasi (JWT)
- Login: `POST /api/v1/users/login` → body `{"email": "...", "password": "..."}` → returns `{"access_token": "...", "refresh_token": "...", "token_type": "bearer"}`
- Refresh: `POST /api/v1/users/refresh` → body `{"refresh_token": "..."}` → returns token baru + refresh token baru
- Akses endpoint terproteksi: header `Authorization: Bearer <token>`
- GET current user: `GET /api/v1/users/me` → returns data user dari token
- Password hashing: bcrypt via `passlib` (`app/services/auth_service.py`)
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
- Role: `admin`, `editor`, `user` (default: `user`)
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

## Penting (sering salah duga)
- `get_current_user` hanya mock; banyak endpoint menggunakannya sebagai dependency.
- Password hashing: SHA-256 via `hashlib` (tanpa salt) di `app/services/user_service.py:28`. Bukan bcrypt/argon2.
- `alembic.ini` sqlalchemy.url di-override dari `settings.DATABASE_URL` di `alembic/env.py`.
- Tidak ada CI/lint/test runner yang terlihat di repo; jangan asumsikan ada checks.

## File kunci
- `app/main.py`
- `app/dependencies.py`
- `app/core/config.py`
- `app/core/database.py`
- `app/services/user_service.py`
- `alembic.ini`, `alembic/env.py`
- `seed_accounts.py`

## Opsional: verifikasi singkat
Kalau mengubah flow auth, pastikan endpoint depend `get_current_user` masih bisa diakses (contoh: `GET /api/v1/users/`).
