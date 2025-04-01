# Local Environment Setup for kernel-planckster

This guide documents how to set up the local development environment for the `kernel-planckster` project. It captures workarounds, platform-specific tweaks, and migration gotchas.

---

## 1. Prerequisites

- Python 3.10 (3.11 also works; avoid 3.12+ due to incompatibilities)
- Homebrew (on macOS)
- Docker + Docker Compose
- PostgreSQL (via Homebrew)

---

## 2. Create the Virtual Environment

```bash
/opt/homebrew/bin/python3.10 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Poetry

Poetry is installed **inside the virtual environment**:

```bash
pip install poetry
```

---

## 4. Fix psycopg2 on Apple Silicon

```bash
brew install libpq --build-from-source
brew install openssl

export LDFLAGS="-L/opt/homebrew/opt/openssl@1.1/lib -L/opt/homebrew/opt/libpq/lib"
export CPPFLAGS="-I/opt/homebrew/opt/openssl@1.1/include -I/opt/homebrew/opt/libpq/include"

pip install psycopg2
```

---

## 5. Fix Poetry Lock Compatibility (virtualenv crash workaround)

Edit `poetry.lock` **before installing dependencies**:

1. Open `poetry.lock`
2. Locate:

   ```toml
   [[package]]
   name = "virtualenv"
   version = "20.24.5"
   ```

3. Replace with:

   ```toml
   version = "20.30.0"
   ```

4. Save the file.

5. Run:

   ```bash
   poetry lock --no-update
   poetry install
   ```

This avoids a crash on Python 3.10+ caused by `virtualenv` using deprecated internals.

---

## 6. Pre-commit Hooks

```bash
pre-commit install
pre-commit run --all-files
```

---

## 7. Run the Development Stack

```bash
docker compose --profile dev up -d
```

---

## 8. Database Migrations

```bash
# Apply migrations:
alembic upgrade head

# Generate a new migration:
alembic revision --autogenerate -m "<your message>"
alembic upgrade head

# Downgrade for testing:
alembic downgrade base
```

### ⚠️ Downgrade Enum Fix

If you see:

```
psycopg2.errors.DependentObjectsStillExist: cannot drop type <enum> because other objects depend on it
```

Fix the `downgrade()` in the relevant Alembic revision file:

```python
op.alter_column(
    "message_content",
    "content_type",
    type_=sa.String(),
    postgresql_using="content_type::text"
)

sa.Enum(name="messagecontenttypeenum").drop(op.get_bind(), checkfirst=True)
```

This detaches the enum from the column before dropping it.

---

## 9. Set Environment Variables

Before running the development server, set the following environment variables:

```bash
export KP_MODE=development
export KP_FASTAPI_HOST=0.0.0.0
export KP_FASTAPI_PORT=8000
export KP_FASTAPI_RELOAD=false
export KP_RDBMS_HOST=localhost
export KP_RDBMS_PORT=5432
export KP_RDBMS_DBNAME=kp-db
export KP_RDBMS_USERNAME=postgres
export KP_RDBMS_PASSWORD=postgres
export KP_OBJECT_STORE_HOST=localhost
export KP_OBJECT_STORE_PORT=9001
export KP_OBJECT_STORE_ACCESS_KEY=minio
export KP_OBJECT_STORE_SECRET_KEY=minio123
export KP_OBJECT_STORE_BUCKET=default
export KP_OBJECT_STORE_SIGNED_URL_EXPIRY=60
```

You can place these in a `.env` file if the project supports it, or add them to your shell config for persistence.

---

## 10. Run the Dev Server

```bash
poetry run dev
```

---

## 11. Access the API Documentation

Once the server is running, FastAPI automatically provides interactive documentation:

- **Swagger UI** for testing endpoints: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc UI** for structured documentation: [http://localhost:8000/redoc](http://localhost:8000/redoc)

These UIs are helpful for manually testing and understanding the available API endpoints.

---

## Done!

Your environment is now ready to develop, test, and run `kernel-planckster` locally.
