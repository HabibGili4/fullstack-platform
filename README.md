# latihan-fastapi

REST API dibangun dengan FastAPI — belajar arsitektur modular, validasi data, dan dependency injection.

## Tech Stack

- Python 3.11+
- FastAPI
- Pydantic / Pydantic Settings

## Fitur

- **Routing Modular** — setiap resource punya file sendiri di `app/api/`
- **Schema Validation** — validasi request body dengan Pydantic + field_validator
- **Dependency Injection** — reusable function untuk auth mockup & pagination
- **Environment Config** — konfigurasi via `.env` dengan pydantic-settings
- **HTTP Exception** — handling 404 dengan pesan yang jelas

## Project Structure

```
latihan-fastapi/
├── .env                  ← environment variables
├── .env.example          ← template .env
├── pyproject.toml        ← dependencies
│
└── app/
    ├── main.py           ← entry point
    ├── dependencies.py   ← get_current_user, get_pagination
    │
    ├── api/
    │   ├── health.py     ← GET /api/v1/health
    │   ├── users.py      ← GET, POST /api/v1/users
    │   └── products.py   ← GET /api/v1/products
    │
    ├── core/
    │   └── config.py     ← Settings
    │
    ├── schemas/
    │   └── user.py       ← UserCreate, UserResponse
    │
    ├── models/           ← (database models nanti)
    ├── repositories/     ← (repository nanti)
    └── services/         ← (business logic nanti)
```

## Setup

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

## API Endpoints

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/api/v1/health/` | Health check |
| GET | `/api/v1/users/` | Dapatkan semua users |
| GET | `/api/v1/users/{user_id}` | Dapatkan user by ID |
| POST | `/api/v1/users/` | Registrasi user baru |
| GET | `/api/v1/products/` | Dapatkan products (pagination) |
| GET | `/api/v1/products/{product_id}` | Dapatkan product by ID |
| GET | `/api/v1/products/price/{price}` | Dapatkan product by price |

## Contoh Request / Response

### POST /api/v1/users/

**Request:**

```json
{
    "name": "Aji",
    "email": "aji@example.com",
    "age": 20,
    "password": "secret123"
}
```

**Response (201):**

```json
{
    "name": "Aji",
    "email": "aji@example.com",
    "age": 20
}
```

> Password tidak dikembalikan di response.

### GET /api/v1/users/1

**Response (200):**

```json
{
    "id": 1,
    "name": "Habib",
    "user": {
        "id": 1,
        "name": "Habib"
    }
}
```

### GET /api/v1/users/999

**Response (404):**

```json
{
    "detail": "pengguna tidak ditemukan"
}
```

### GET /api/v1/products/?page=2&limit=5&category=electronics

**Response (200):**

```json
{
    "page": 2,
    "limit": 5,
    "category": "electronics",
    "search": null,
    "user": {
        "id": 1,
        "name": "Habib"
    }
}
```

## Configuration

| Variable | Tipe | Deskripsi |
|----------|------|-----------|
| `DATABASE_URL` | string | URL koneksi database |
| `SECRET_KEY` | string | Secret key untuk aplikasi |
| `DEBUG` | boolean | Mode debug (default: false) |

## License

MIT
