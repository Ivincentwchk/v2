# CSCI3100 Backend (v2)

This project is a Dockerized Django REST API backed by PostgreSQL.

---

## Database Initialization with SQL Files

The repository contains SQL scripts under the `sqls/` folder for initializing the database with subjects, courses, and other data.

These scripts are **not** run automatically by Docker. Each developer must run them manually when setting up their local database.

### 1. Start the Docker stack

From the project root (`v2`):

```bash
docker compose up --build
```

Wait until:
- The Postgres container (`csci3100_db_server`) is running.
- The Django API and pgAdmin (if used) are up.

### 2. Connect to PostgreSQL

Use either **pgAdmin** or `psql`.

#### Option A: Using pgAdmin (GUI)

1. Open pgAdmin in your browser:
   - `http://localhost:8080/`
2. Log in using the credentials from `.env`:
   - `PGADMIN_DEFAULT_EMAIL`
   - `PGADMIN_DEFAULT_PASSWORD`
3. Register a new server pointing to the Postgres service:
   - Host: `csci3100_db_server` (or `localhost` with forwarded port `5432`)
   - Port: `5432`
   - Username: `POSTGRES_USER` from `.env`
   - Password: `POSTGRES_PASSWORD` from `.env`
4. Open the Query Tool and run the SQL files from the `sqls/` directory (copy & paste or use the file open dialog):
   - `sqls/subject_course.sql`
   - `sqls/git.sql`
   - `sqls/docker.sql`

#### Option B: Using psql (CLI)

If you have `psql` installed locally, you can connect directly to the Dockerized database. From the host machine:

```bash
psql "host=localhost port=5432 dbname=$POSTGRES_DB user=$POSTGRES_USER password=$POSTGRES_PASSWORD"
```

Then inside `psql`, execute the SQL files (adjust the path if needed):

```sql
\i sqls/subject_course.sql;
\i sqls/git.sql;
\i sqls/docker.sql;
```

Alternatively, you can run `psql` inside the Postgres container, for example:

```bash
docker compose exec csci3100_db_server psql -U $POSTGRES_USER -d $POSTGRES_DB -f /docker-entrypoint-initdb.d/subject_course.sql
```

(repeat for `git.sql` and `docker.sql` as needed, or copy them somewhere inside the container.)

### 3. Verifying the data

After running the scripts, verify that the data is present, for example:

```sql
SELECT * FROM accounts_subject;
SELECT * FROM accounts_course;
```

You should see rows corresponding to the test data defined in the SQL files.

---

## Notes

- Running the SQL scripts multiple times may cause primary key or duplicate-data errors. For a clean re-init:
  1. Stop containers: `docker compose down`
  2. Remove the Postgres volume (this **deletes all DB data**): `docker volume rm v2_postgres_data_v2`
  3. Start again: `docker compose up --build`
  4. Re-run the SQL scripts as described above.
- API usage and endpoints are documented in `django-api/API_USAGE.md`.
