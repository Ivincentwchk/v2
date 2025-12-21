from django.core.management.base import BaseCommand

from accounts.models import User


class Command(BaseCommand):
    help = "Assign leaderboard ranks based on profile scores (descending)."

    def handle(self, *args, **options):
        users = (
            User.objects.select_related("profile")
            .order_by("-profile__score", "profile__rank", "user_name")
        )

        updated = 0
        for idx, user in enumerate(users, start=1):
            profile = user.profile
            if profile.rank != idx:
                profile.rank = idx
                profile.save(update_fields=["rank"])
                updated += 1

        self.stdout.write(self.style.SUCCESS(f"Updated rank for {updated} user(s)."))
