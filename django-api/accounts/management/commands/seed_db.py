from __future__ import annotations

from io import StringIO
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import connection, transaction

from accounts.models import Course, Option, Question, Subject


class Command(BaseCommand):
    help = "Seed database tables from bundled SQL files."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Run seeding even if the database already appears to contain seed data.",
        )
        parser.add_argument(
            "--sql-dir",
            default="/sqls",
            help="Directory containing seed SQL files (default: /sqls).",
        )

    def handle(self, *args, **options):
        force: bool = options["force"]
        sql_dir = Path(options["sql_dir"]).resolve()

        if not force and (Subject.objects.exists() or Course.objects.exists() or Question.objects.exists() or Option.objects.exists()):
            self.stdout.write(self.style.WARNING("Seed data appears to exist; skipping (use --force to re-run)."))
            return

        db_seed_sql = sql_dir / "db_seed.sql"
        seed_sql = sql_dir / "seed.sql"

        using_db_seed = db_seed_sql.exists()

        if using_db_seed:
            sql_files = [db_seed_sql]
        elif seed_sql.exists():
            sql_files = [seed_sql]
        else:
            sql_files = [
                sql_dir / "subject_course.sql",
                sql_dir / "git.sql",
                sql_dir / "docker.sql",
            ]

        missing = [str(p) for p in sql_files if not p.exists()]
        if missing:
            raise FileNotFoundError(f"Missing SQL seed files: {', '.join(missing)}")

        self.stdout.write(f"Seeding from: {', '.join([p.name for p in sql_files])}")

        with transaction.atomic():
            with connection.cursor() as cursor:
                if using_db_seed:
                    self.stdout.write("Resetting public schema before applying db_seed.sql")
                    cursor.execute("DROP SCHEMA IF EXISTS public CASCADE;")
                    cursor.execute("CREATE SCHEMA public AUTHORIZATION CURRENT_USER;")
                    cursor.execute("GRANT ALL ON SCHEMA public TO CURRENT_USER;")
                    cursor.execute("GRANT ALL ON SCHEMA public TO public;")
                    cursor.execute("COMMENT ON SCHEMA public IS 'standard public schema';")

                for sql_path in sql_files:
                    self._execute_sql_file(cursor, sql_path)

        self.stdout.write(self.style.SUCCESS("Database seed completed."))

    def _execute_sql_file(self, cursor, sql_path: Path) -> None:
        copy_sql: str | None = None
        copy_buffer: list[str] = []
        statement_buffer: list[str] = []

        with sql_path.open(encoding="utf-8") as sql_file:
            for raw_line in sql_file:
                line = raw_line.rstrip("\n")

                if copy_sql is not None:
                    if line == r"\.":
                        data_stream = StringIO("".join(copy_buffer))
                        cursor.copy_expert(copy_sql, data_stream)
                        copy_sql = None
                        copy_buffer = []
                    else:
                        copy_buffer.append(raw_line)
                    continue

                statement_buffer.append(raw_line)
                stripped = line.strip()

                if not stripped or stripped.startswith("--"):
                    continue

                if ";" not in line:
                    continue

                statement = "".join(statement_buffer).strip()
                statement_buffer = []

                if not statement:
                    continue

                clean_lines = [ln for ln in statement.splitlines() if not ln.strip().startswith("--")]
                clean_statement = "\n".join(clean_lines).strip()

                if not clean_statement:
                    continue

                upper_stmt = clean_statement.upper()
                if upper_stmt.startswith("COPY ") and "FROM STDIN" in upper_stmt:
                    copy_sql = clean_statement
                    copy_buffer = []
                    continue

                cursor.execute(clean_statement)

            trailing = "\n".join([ln for ln in "".join(statement_buffer).splitlines() if not ln.strip().startswith("--")]).strip()
            if trailing:
                cursor.execute(trailing)
