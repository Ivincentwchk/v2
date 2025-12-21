from django.utils import timezone
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import Achievement, Question, SubjectBookmark, UserAchievement, UserCourse


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def achievements(request):
    user = request.user
    profile = user.profile

    login_streak = int(profile.login_streak_days or 0)
    completed_course_ids = set(
        UserCourse.objects.filter(UserID=user, CourseFlag='completed').values_list('CourseID_id', flat=True)
    )

    definitions = []
    login_targets = [5, 10, 50, 100, 365, 500]
    for target in login_targets:
        definitions.append({
            'key': f'login_streak_{target}',
            'category': 'login_streak',
            'title': f'Login Streak {target}',
            'description': f'Log in for {target} days in a row.',
            'icon': 'streak',
            'target': target,
            'compute': lambda t=target: (min(login_streak, t), login_streak >= t, {}),
        })

    newbie_specs = [
        ('docker_newbie', 'Docker Newbie', {20, 21}, 'docker'),
        ('git_newbie', 'Git Newbie', {10, 11}, 'git'),
    ]
    for key, title, required, icon in newbie_specs:
        definitions.append({
            'key': key,
            'category': 'course_newbie',
            'title': title,
            'description': 'Finish the intro courses 1 and 2.',
            'icon': icon,
            'target': len(required),
            'compute': lambda req=required: (
                len(req.intersection(completed_course_ids)),
                req.issubset(completed_course_ids),
                {'required_course_ids': sorted(req)},
            ),
        })

    results = []
    with transaction.atomic():
        for spec in definitions:
            progress, unlocked, meta = spec['compute']()
            achievement, _ = Achievement.objects.get_or_create(
                key=spec['key'],
                defaults={
                    'category': spec['category'],
                    'title': spec['title'],
                    'description': spec['description'],
                    'icon': spec['icon'],
                    'target': spec['target'],
                    'metadata': meta,
                },
            )

            if achievement.target != spec['target'] or achievement.title != spec['title'] or achievement.description != spec['description'] or achievement.icon != spec['icon'] or achievement.category != spec['category']:
                achievement.category = spec['category']
                achievement.title = spec['title']
                achievement.description = spec['description']
                achievement.icon = spec['icon']
                achievement.target = spec['target']
                achievement.metadata = meta
                achievement.save()

            ua, _ = UserAchievement.objects.get_or_create(user=user, achievement=achievement)
            ua.progress = int(progress)
            if unlocked and not ua.unlocked:
                ua.unlocked = True
                ua.unlocked_at = timezone.now()
            if not unlocked and ua.unlocked:
                ua.unlocked = False
                ua.unlocked_at = None
            ua.save()

            payload = {
                'id': achievement.key,
                'type': achievement.category,
                'title': achievement.title,
                'description': achievement.description,
                'icon': achievement.icon,
                'target': achievement.target,
                'progress': ua.progress,
                'unlocked': ua.unlocked,
            }
            if achievement.metadata:
                payload.update(achievement.metadata)
            results.append(payload)

    return Response({'login_streak_days': login_streak, 'achievements': results})
