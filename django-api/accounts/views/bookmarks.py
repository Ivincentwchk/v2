from django.utils import timezone
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import Subject, SubjectBookmark, UserActivity


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_bookmarked_subject(request):
    subject_id = request.data.get('subject_id')
    if subject_id is None:
        return Response({'detail': 'subject_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        subject_id_int = int(subject_id)
    except (TypeError, ValueError):
        return Response({'detail': 'subject_id must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        subject = Subject.objects.get(pk=subject_id_int)
    except Subject.DoesNotExist:
        return Response({'detail': 'Subject not found.'}, status=status.HTTP_404_NOT_FOUND)

    profile = request.user.profile
    profile.bookmarked_subject = subject
    profile.bookmarked_subject_updated_at = timezone.now()
    profile.save(update_fields=['bookmarked_subject', 'bookmarked_subject_updated_at'])

    with transaction.atomic():
        SubjectBookmark.objects.filter(user=request.user, subject=subject).delete()
        SubjectBookmark.objects.create(user=request.user, subject=subject)

        keep_ids = (
            SubjectBookmark.objects.filter(user=request.user)
            .order_by('-created_at')
            .values_list('id', flat=True)[:5]
        )
        SubjectBookmark.objects.filter(user=request.user).exclude(id__in=list(keep_ids)).delete()

    UserActivity.objects.create(
        user=request.user,
        activity_type='SCORE_UPDATE',
        details=f"Bookmarked subject set: {subject_id_int}",
    )

    return Response(
        {
            'bookmarked_subject_id': subject.SubjectID,
            'bookmarked_subject_name': subject.SubjectName,
            'bookmarked_subject_updated_at': profile.bookmarked_subject_updated_at,
        }
    )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_bookmarked_subject(request, subject_id):
    try:
        subject_id_int = int(subject_id)
    except (TypeError, ValueError):
        return Response({'detail': 'subject_id must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        SubjectBookmark.objects.filter(user=request.user, subject_id=subject_id_int).delete()

        latest = (
            SubjectBookmark.objects.filter(user=request.user)
            .select_related('subject')
            .order_by('-created_at')
            .first()
        )

        profile = request.user.profile
        if latest is None:
            profile.bookmarked_subject = None
            profile.bookmarked_subject_updated_at = timezone.now()
            profile.save(update_fields=['bookmarked_subject', 'bookmarked_subject_updated_at'])
            return Response({'detail': 'removed', 'bookmarked_subject_id': None})

        profile.bookmarked_subject = latest.subject
        profile.bookmarked_subject_updated_at = timezone.now()
        profile.save(update_fields=['bookmarked_subject', 'bookmarked_subject_updated_at'])

    return Response(
        {
            'detail': 'removed',
            'bookmarked_subject_id': profile.bookmarked_subject.SubjectID,
            'bookmarked_subject_name': profile.bookmarked_subject.SubjectName,
            'bookmarked_subject_updated_at': profile.bookmarked_subject_updated_at,
        }
    )
