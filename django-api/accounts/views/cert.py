from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import Course, Subject, UserCertificate, UserCourse


def _serialize_certificate(cert: UserCertificate | None):
    if cert is None:
        return None

    return {
        "subject": {
            "id": cert.subject.SubjectID if cert.subject else None,
            "name": cert.subject.SubjectName if cert.subject else None,
        },
        "name_en": cert.name_en,
        "name_cn": cert.name_cn,
        "subject_en": cert.subject_en,
        "subject_cn": cert.subject_cn,
        "course_titles": cert.course_titles,
        "completed_at": cert.completed_at,
        "first_downloaded_at": cert.first_downloaded_at,
        "metadata": cert.metadata,
    }


def _completed_courses_queryset(user):
    return UserCourse.objects.filter(UserID=user, CourseFlag='completed').select_related('CourseID__SubjectID')


def _get_subject(subject_id):
    try:
        subject_pk = int(subject_id)
    except (TypeError, ValueError):
        raise ValueError("subject_id must be an integer.")
    return get_object_or_404(Subject, pk=subject_pk)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def certificate_status(request):
    user = request.user
    subject_id = request.query_params.get("subject_id")
    if not subject_id:
        return Response({"detail": "subject_id query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        subject = _get_subject(subject_id)
    except ValueError as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    subject_courses = Course.objects.filter(SubjectID=subject)
    subject_total = subject_courses.count()
    completed_qs = _completed_courses_queryset(user).filter(CourseID__SubjectID=subject)
    completed_count = completed_qs.count()
    eligible = subject_total > 0 and completed_count >= subject_total

    cert = UserCertificate.objects.filter(user=user, subject=subject).first()
    completed_course_detail = [
        {
            "course_id": uc.CourseID_id,
            "course_title": uc.CourseID.CourseTitle,
            "score": uc.CourseScore,
        }
        for uc in completed_qs
    ]

    return Response(
        {
            "eligible": eligible,
            "subject": {
                "id": subject.SubjectID,
                "name": subject.SubjectName,
                "total_courses": subject_total,
                "completed_courses": completed_count,
            },
            "completed_courses": completed_course_detail,
            "certificate": _serialize_certificate(cert),
        }
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def certificate_download(request):
    user = request.user
    subject_id = request.data.get("subject_id")
    if subject_id is None or subject_id == "":
        subject_id = request.query_params.get("subject_id")

    if subject_id is None or subject_id == "":
        return Response({"detail": "subject_id is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        subject = _get_subject(subject_id)
    except ValueError as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    subject_courses = Course.objects.filter(SubjectID=subject)
    subject_total = subject_courses.count()
    completed_courses = list(_completed_courses_queryset(user).filter(CourseID__SubjectID=subject))
    completed_count = len(completed_courses)

    if subject_total == 0 or completed_count < subject_total:
        return Response(
            {"detail": "Complete all courses in this subject before downloading the certificate."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    with transaction.atomic():
        cert, _ = UserCertificate.objects.select_for_update().get_or_create(user=user, subject=subject)
        if cert.first_downloaded_at is None:
            now = timezone.now()
            course_titles = [uc.CourseID.CourseTitle for uc in completed_courses]
            course_scores = [
                {
                    "course_id": uc.CourseID_id,
                    "course_title": uc.CourseID.CourseTitle,
                    "score": uc.CourseScore,
                }
                for uc in completed_courses
            ]

            cert.name_en = request.data.get("name_en") or user.user_name
            cert.name_cn = request.data.get("name_cn") or cert.name_en
            cert.subject_en = request.data.get("subject_en") or subject.SubjectName
            cert.subject_cn = request.data.get("subject_cn") or cert.subject_en
            cert.course_titles = course_titles
            cert.completed_at = now
            cert.first_downloaded_at = now
            cert.metadata = {"course_scores": course_scores}
            cert.save()

    return Response(
        {
            "eligible": True,
            "subject": {
                "id": subject.SubjectID,
                "name": subject.SubjectName,
                "total_courses": subject_total,
                "completed_courses": completed_count,
            },
            "certificate": _serialize_certificate(cert),
        }
    )
