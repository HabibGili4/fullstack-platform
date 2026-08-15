# latihan-fastapi

REST API dibangun dengan FastAPI — belajar arsitektur modular, autentikasi JWT, RBAC, Docker, dan testing suite.

## Tech Stack

| Category | Tech |
|----------|------|
| Language | Python 3.11+ |
| Framework | FastAPI |
| Validation | Pydantic / Pydantic Settings |
| Auth | python-jose (JWT HS256), passlib (bcrypt) |
| Database | PostgreSQL, SQLAlchemy 2.0, psycopg2-binary |
| Migrations | Alembic |
| Package Manager | uv |
| Testing | pytest, httpx, pytest-cov |
| Container | Docker, Docker Compose |

## Fitur

- **JWT Authentication** — login, refresh token, GET /me
- **Role-Based Access Control (RBAC)** — admin, manager, editor, user
- **Products CRUD** — create, read, update, delete dengan ownership validation
- **Posts CRUD** — create, read, update, delete
- **Tasks CRUD** — dengan RBAC permissions
- **Accounts** — transfer between accounts
- **Logging Management** — INFO / WARNING / ERROR levels
- **Docker Support** — Dockerfile + docker-compose (app + PostgreSQL)
- **Testing Suite** — 64 tests (unit, integration, E2E), 85% coverage
- **Service/Repository Pattern** — separation of concerns

## Project Structure

```
latihan-fastapi/
├── .env                    ← environment variables
├── .env.example            ← template .env
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml          ← dependencies
├── alembic.ini
├── seed_accounts.py        ← seed data accounts
├── seed_roles.py           ← seed data users with roles
│
├── app/
│   ├── main.py             ← entry point + lifespan
│   ├── core/
│   │   ├── config.py       ← Settings (pydantic-settings)
│   │   ├── database.py     ← engine + get_db
│   │   ├── logging.py      ← setup_logging
│   │   ├── permissions.py  ← ROLE_PERMISSIONS
│   │   └── ports.py        ← interfaces (IPasswordHasher, ITokenService)
│   ├── dependencies/
│   │   ├── auth.py         ← get_current_user (JWT Bearer)
│   │   ├── services.py     ← DI factories
│   │   ├── permissions.py  ← require_permission()
│   │   └── pagination.py   ← get_pagination
│   ├── api/
│   │   ├── health.py
│   │   ├── users.py
│   │   ├── products.py
│   │   ├── posts.py
│   │   ├── tasks.py
│   │   └── accounts.py
│   ├── models/             ← SQLAlchemy models
│   ├── schemas/            ← Pydantic schemas
│   ├── repositories/       ← DB operations
│   └── services/           ← Business logic
│
└── tests/
    ├── conftest.py
    ├── unit/services/      ← unit tests (mock dependencies)
    ├── unit/repositories/  ← repository tests (real DB)
    ├── integration/api/    ← API endpoint tests
    ├── integration/database/ ← DB connection tests
    └── e2e/                ← end-to-end flow tests
```

## Setup

### Local Development

```bash
# 1. Clone
git clone git@github.com:HabibGili4/fullstack-platform.git
cd fullstack-platform

# 2. Install dependencies
uv sync

# 3. Copy .env
cp .env.example .env

# 4. Jalankan server
uv run uvicorn app.main:app --reload
```

Buka http://localhost:8000/docs untuk Swagger UI.

### Docker

```bash
# Build & start (background)
docker compose up --build -d

# Akses app
curl http://localhost:8001/

# Logs
docker compose logs -f app

# Stop
docker compose down

# Stop + hapus data
docker compose down -v
```

Buka http://localhost:8001/docs untuk Swagger UI.

## API Endpoints

### Root & Health

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | Root endpoint | - |
| GET | `/api/v1/health/` | Health check | - |

### Users

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/users/login` | Login → JWT tokens | - |
| POST | `/api/v1/users/refresh` | Refresh access token | - |
| GET | `/api/v1/users/me` | Get current user profile | Bearer JWT |
| GET | `/api/v1/users/` | List all users | Bearer JWT |
| GET | `/api/v1/users/{user_id}` | Get user by ID | Bearer JWT |
| POST | `/api/v1/users/` | Register new user | - |
| PUT | `/api/v1/users/{user_id}` | Update user | Bearer JWT |
| DELETE | `/api/v1/users/{user_id}` | Delete user | Bearer JWT |

### Products

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| GET | `/api/v1/products/` | List all products | `product:read` |
| GET | `/api/v1/products/{product_id}` | Get product by ID | `product:read` |
| POST | `/api/v1/products/` | Create product | `product:create` |
| PUT | `/api/v1/products/{product_id}` | Update product | `product:update` |
| DELETE | `/api/v1/products/{product_id}` | Delete product | `product:delete` |

### Posts

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/posts/` | List all posts | Bearer JWT |
| GET | `/api/v1/posts/{post_id}` | Get post by ID | Bearer JWT |
| GET | `/api/v1/posts/user/{user_id}` | Get posts by user | Bearer JWT |
| POST | `/api/v1/posts/` | Create post | Bearer JWT |
| PUT | `/api/v1/posts/{post_id}` | Update post | Bearer JWT |
| DELETE | `/api/v1/posts/{post_id}` | Delete post | Bearer JWT |

### Tasks

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| GET | `/api/v1/tasks/` | List all tasks | `task:view` |
| GET | `/api/v1/tasks/{task_id}` | Get task by ID | `task:view` |
| GET | `/api/v1/tasks/user/{user_id}` | Get tasks by user | `task:view` |
| POST | `/api/v1/tasks/` | Create task | `task:create` |
| PUT | `/api/v1/tasks/{task_id}` | Update task | `task:update` |
| DELETE | `/api/v1/tasks/{task_id}` | Delete task | `task:delete` |

### Accounts

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/accounts/{account_id}` | Get account by ID | Bearer JWT |
| POST | `/api/v1/accounts/transfer` | Transfer between accounts | Bearer JWT |

## Authentication

### Login

```bash
POST /api/v1/users/login
Content-Type: application/json

{
    "email": "admin@test.com",
    "password": "password123"
}
```

**Response:**

```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer"
}
```

### Access Protected Endpoint

```bash
GET /api/v1/users/me
Authorization: Bearer <access_token>
```

### Refresh Token

```bash
POST /api/v1/users/refresh
Content-Type: application/json

{
    "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

## Role-Based Access Control (RBAC)

| Role | Products | Tasks |
|------|----------|-------|
| **admin** | read, create, update, delete | view, create, update, delete |
| **manager** | - | view, create, update |
| **editor** | read, create, update | - |
| **user** | read | - |

Seed test users:

```bash
uv run python seed_roles.py
```

| Name | Email | Password | Role |
|------|-------|----------|------|
| Admin User | admin@test.com | password123 | admin |
| Manager User | manager@test.com | password123 | manager |
| Editor User | editor@test.com | password123 | editor |
| Regular User | user@test.com | password123 | user |

## Configuration

### Environment Variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `DATABASE_URL` | string | Yes | - | PostgreSQL connection URL |
| `SECRET_KEY` | string | Yes | - | JWT signing secret |
| `DEBUG` | boolean | No | `false` | Debug mode |
| `LOG_LEVEL` | string | No | `INFO` | Logging level |

### JWT Settings (hardcoded in config.py)

| Setting | Value |
|---------|-------|
| Algorithm | HS256 |
| Access token expiry | 30 minutes |
| Refresh token expiry | 7 days |

## Testing

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=app --cov-report=term-missing

# Run specific test type
uv run pytest tests/unit/ -v
uv run pytest tests/integration/ -v
uv run pytest tests/e2e/ -v
```

### Test Structure

| Type | Description | Count |
|------|-------------|-------|
| Unit | Service & repository tests (mock dependencies) | 22 |
| Integration | API endpoint tests (real DB) | 22 |
| E2E | Full user journey tests | 5 |
| Security Matrix | Auth & RBAC edge cases | 15 |
| **Total** | | **64** |

## Seed Data

```bash
# Seed bank accounts (for transfer demo)
uv run python seed_accounts.py

# Seed users with different roles (for RBAC testing)
uv run python seed_roles.py
```

## License

MIT
