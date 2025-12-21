from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import User


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rank(request):
    """
    Return leaderboard data ordered by profile.score (desc) then profile.rank.

    - Always returns up to 10 rows.
    - If the caller isn't in the top 10, their row is appended.
    - Each row also includes a computed `position`.
    """

    user = request.user

    ordered_users = list(
        User.objects.select_related('profile')
        .order_by('-profile__score', 'profile__rank', 'user_name')
    )

    def serialize_user(u, position):
        profile = getattr(u, 'profile', None)
        return {
            'user_name': u.user_name,
            'rank': getattr(profile, 'rank', None) if profile is not None else None,
            'score': getattr(profile, 'score', 0) if profile is not None else 0,
            'position': position,
        }

    top_users = ordered_users[:10]
    data = [serialize_user(u, idx + 1) for idx, u in enumerate(top_users)]

    for entry in data:
        if entry['user_name'] == user.user_name:
            return Response(data)

    # Caller not in top 10; append their row if they exist in the table.
    try:
        caller_index = next(idx for idx, u in enumerate(ordered_users) if u.pk == user.pk)
        caller_serialized = serialize_user(ordered_users[caller_index], caller_index + 1)
        data.append(caller_serialized)
    except StopIteration:
        # User might not have a profile row; fall back to zero score at end.
        data.append(
            {
                'user_name': user.user_name,
                'rank': getattr(getattr(user, 'profile', None), 'rank', None),
                'score': getattr(getattr(user, 'profile', None), 'score', 0),
                'position': None,
            }
        )

    return Response(data)
