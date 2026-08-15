# ============================================
# STAGE 1: builder
# Install dependencies
# ============================================
FROM python:3.11-slim AS builder

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock .python-version README.md ./

ENV UV_PROJECT_ENVIRONMENT="/usr/local"
RUN uv sync --no-dev

# ============================================
# STAGE 2: runtime
# Only Python + deps + app code (no uv)
# ============================================
FROM python:3.11-slim AS runtime

WORKDIR /app

# Copy installed packages dari builder
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn

# Copy application code
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini ./
COPY seed_accounts.py seed_roles.py ./

# Non-root user
RUN addgroup --system app && adduser --system --ingroup app app
RUN chown -R app:app /app
USER app

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
