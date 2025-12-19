from __future__ import annotations

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

        seed_sql = sql_dir / "seed.sql"
        if seed_sql.exists():
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
                for sql_path in sql_files:
                    self._execute_sql_file(cursor, sql_path)

        self.stdout.write(self.style.SUCCESS("Database seed completed."))

    def _execute_sql_file(self, cursor, sql_path: Path) -> None:
        sql = sql_path.read_text(encoding="utf-8")
        statements = [stmt.strip() for stmt in sql.split(";") if stmt.strip()]

        for stmt in statements:
            cursor.execute(stmt)
