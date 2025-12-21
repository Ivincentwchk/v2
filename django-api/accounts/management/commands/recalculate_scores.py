from django.core.management.base import BaseCommand
from django.db.models import IntegerField, Sum
from django.db.models.functions import Cast

from accounts.models import UserCourse, User


class Command(BaseCommand):
    help = "Recalculate each user's profile.score from their completed courses."

    def handle(self, *args, **options):
        users = User.objects.select_related("profile")
        updated = 0

        for user in users:
            total = (
                UserCourse.objects.filter(UserID=user, CourseFlag="completed")
                .annotate(score_int=Cast("CourseScore", IntegerField()))
                .aggregate(total_score=Sum("score_int"))
                .get("total_score")
            )

            total_score = total or 0

            if user.profile.score != total_score:
                user.profile.score = total_score
                user.profile.save(update_fields=["score"])
                updated += 1

        self.stdout.write(self.style.SUCCESS(f"Updated scores for {updated} user(s)."))
