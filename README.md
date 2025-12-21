# CSCI3100 Project Backend (Docker + pgAdmin)

This backend ships with a Docker Compose stack that provisions:

1. **PostgreSQL** database (`csci3100_db_server`)
2. **Django API** service (`api`)
3. **pgAdmin 4** GUI (`gui`) for convenient database inspection

The instructions below explain how to launch the stack, run the server, and connect through pgAdmin.

---

## 1. Prerequisites

- Docker Desktop (or Docker Engine) and Docker Compose v2
- Copy the example environment file and adjust it for your machine:

```bash
cp .env.example .env
```

Ensure the following values are set:

| Variable | Description |
| --- | --- |
| `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` | Database name and credentials used by both PostgreSQL and Django |
| `DJANGO_SECRET_KEY`, `DJANGO_DEBUG` | Usual Django settings |
| `DATABASE_URL_FORMATTED` | Connection string Django uses to reach Postgres (`postgresql://user:pass@csci3100_db_server:5432/db`) |
| `PGADMIN_DEFAULT_EMAIL`, `PGADMIN_DEFAULT_PASSWORD` | Login for pgAdmin GUI |

### Repository layout

```
backend/
├── django-api/        # Django project source (manage.py lives here)
├── sqls/              # Seed SQL: db_seed.sql snapshot + legacy seed scripts
├── scripts/           # Helper utilities (e.g., backup-db.sh)
├── docker-compose.yml # Compose stack for Postgres + API + pgAdmin
└── README.md
```

---

## 2. Starting the services

From the repo root (`CSCI3100_project_backend_v2`), run:

```bash
docker compose up --build
```

What happens:

- PostgreSQL starts first and exposes port **5432**
- Once Postgres is healthy, the Django `api` container runs `python manage.py migrate` and then starts the dev server on **http://localhost:8000**
- pgAdmin becomes available on **http://localhost:8080**
- Database files persist inside the named volume `postgres_data_v2`

Need to run the containers in the background? Append `-d`:

```bash
docker compose up --build -d
```

To stop everything and remove containers (but keep the volume):

```bash
docker compose down
```

---

## 3. Interacting with the Django API

- API base URL: **http://localhost:8000**
- The container automatically applies migrations on boot. To run extra management commands:

```bash
docker compose exec api python manage.py createsuperuser
docker compose exec api python manage.py shell
```

Logs for each service:

```bash
docker compose logs -f api          # Django
docker compose logs -f csci3100_db_server
docker compose logs -f gui          # pgAdmin
```

---

## 4. Using pgAdmin (web UI for PostgreSQL)

1. Navigate to **http://localhost:8080**
2. Sign in with the credentials defined in `.env` (`PGADMIN_DEFAULT_EMAIL` / `PGADMIN_DEFAULT_PASSWORD`)
3. Add a new server:
   - **Name:** anything (e.g., `Local CS3100`)
   - **Connection Tab:**
     - Host name/address: `csci3100_db_server` (container name resolves within Docker network)
     - Port: `5432`
     - Maintenance DB: value from `POSTGRES_DB`
     - Username: value from `POSTGRES_USER`
     - Password: value from `POSTGRES_PASSWORD`
4. Save to connect. You can now browse schemas, run SQL queries, inspect tables, etc.

> ℹ️ If you prefer connecting from a local client (psql, DBeaver, etc.), use `localhost:5432` with the same credentials because Postgres is published to the host.

---

## 5. Database seed (export & restore)

The Django management command now **auto-detects `sqls/db_seed.sql`**. When that file exists, `python manage.py seed_db` will:

1. Drop and recreate the `public` schema (inside a transaction) so the dump can replay cleanly.
2. Stream the dump, including `COPY ... FROM stdin` sections, directly into Postgres.

This happens automatically during `docker compose up --build` because the `api` service runs `python manage.py seed_db` on boot. No manual `psql` piping is required as long as `db_seed.sql` is present.

### Updating the snapshot

To capture a new snapshot of the live database into `sqls/db_seed.sql`:

```bash
docker compose exec -T csci3100_db_server \
  pg_dump -U django_user -d backend_db \
  --format=plain --no-owner --no-acl \
  > sqls/db_seed.sql
```

On the next `docker compose up --build` (or manual `docker compose exec api python manage.py seed_db --force`), the new dump will be applied automatically.

> Need the legacy, schema-preserving inserts instead? Remove/rename `db_seed.sql` and the seeder will fall back to `seed.sql`, `subject_course.sql`, etc.

### Manual restore (optional)

If you ever want to replay the dump yourself (e.g., outside of Docker), you can still pipe it into psql:

```bash
cat sqls/db_seed.sql | docker compose exec -T csci3100_db_server \
  psql -U django_user -d backend_db
```

> This dump includes schema + data (subjects, courses, questions, icons, seed users, etc.). The `ON CONFLICT` logic from `sqls/subject_course.sql` can still be run separately if you only need subject/course content.

### On-demand backup helper

For “big change” checkpoints, run the helper script:

```bash
./scripts/backup-db.sh
```

It writes a timestamped dump (e.g., `sqls/db_seed_20251221-145700.sql`) and updates `sqls/db_seed_latest.sql` to point at the newest file. You can commit any snapshot you want to preserve (or keep them gitignored if they become large).

---

## 6. Troubleshooting

- **Environment mismatch:** Ensure `.env` and `.env.example` stay in sync. If Postgres refuses connections, double-check `POSTGRES_DB` vs `DATABASE_URL_FORMATTED`.
- **Stale volumes:** To reset the Postgres data volume, run `docker compose down -v` (this erases all data).
- **Mac/Windows port conflicts:** Make sure ports 5432 (Postgres), 8000 (Django), and 8080 (pgAdmin) are unused before starting the stack.
- **Email gateway errors:** When using Gmail, you must create an App Password and paste it into `EMAIL_HOST_PASSWORD`. Regular Gmail passwords are blocked.

---

## 7. Email (Gmail SMTP) setup

1. Create a Gmail App Password (Google Account → Security → App passwords → select “Mail” + “Other”).
2. Update `.env` with:
   ```
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-gmail@gmail.com
   EMAIL_HOST_PASSWORD=the-app-password
   DEFAULT_FROM_EMAIL="CSCI3100 Team <your-gmail@gmail.com>"
   ```
3. Restart the stack (`docker compose up --build`) so Django picks up the new credentials.

These settings enable future features such as “forgot password” emails or license notifications.

### Password reset test endpoint

You can trigger the mock reset flow via the new API route:

```bash
curl -X POST http://localhost:8000/api/accounts/password-reset/ \
  -H "Content-Type: application/json" \
  -d '{
        "email": "user@example.com",
        "reset_base_url": "https://your-frontend/reset-password"
      }'
```

If the email exists in the database, the backend sends a mock reset link pointing at `reset_base_url` with a placeholder token.

With this setup, any teammate can clone the repo, copy `.env.example`, and run `docker compose up --build` to get the API and pgAdmin running within minutes.
