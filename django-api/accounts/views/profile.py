from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import SubjectBookmark, UserCourse
from accounts.serializers import UserSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    serializer = UserSerializer(user)

    recent_bookmarks_qs = (
        SubjectBookmark.objects.filter(user=user)
        .select_related("subject")
        .order_by("-created_at")
        .only("created_at", "subject__SubjectID", "subject__SubjectName", "subject__icon_svg_url")
    )

    recent_bookmarked_subjects = []
    seen_subject_ids = set()
    for bm in recent_bookmarks_qs:
        sid = getattr(bm.subject, "SubjectID", None)
        if sid is None or sid in seen_subject_ids:
            continue
        seen_subject_ids.add(sid)
        recent_bookmarked_subjects.append(
            {
                "subject_id": bm.subject.SubjectID,
                "subject_name": bm.subject.SubjectName,
                "bookmarked_at": bm.created_at,
                "subject_icon_svg_url": bm.subject.icon_svg_url,
            }
        )
        if len(recent_bookmarked_subjects) >= 5:
            break

    completed = UserCourse.objects.filter(UserID=user, CourseFlag="completed").only("CourseID_id", "CourseScore")

    total_score = 0
    completed_course_scores = []
    for item in completed:
        try:
            score_int = int(item.CourseScore)
        except (TypeError, ValueError):
            score_int = 0
        total_score += score_int
        completed_course_scores.append({"CourseID": item.CourseID_id, "CourseScore": score_int})

    data = serializer.data
    try:
        if data.get("profile") is not None:
            data["profile"]["profile_pic_url"] = request.build_absolute_uri("profile-pic/")
    except Exception:
        pass
    data["total_score"] = total_score
    data["completed_course_scores"] = completed_course_scores
    data["recent_bookmarked_subjects"] = recent_bookmarked_subjects
    return Response(data)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def me_profile_pic(request):
    profile = request.user.profile

    if request.method == "GET":
        if not profile.profile_pic:
            return Response({"detail": "No profile picture."}, status=status.HTTP_404_NOT_FOUND)

        content_type = profile.profile_pic_mime or "application/octet-stream"
        response = HttpResponse(bytes(profile.profile_pic), content_type=content_type)
        response["Cache-Control"] = "no-store"
        return response

    if request.method == "DELETE":
        profile.profile_pic = None
        profile.profile_pic_mime = None
        profile.save(update_fields=["profile_pic", "profile_pic_mime"])
        return Response({"detail": "Profile picture removed."})

    upload = request.FILES.get("file")
    if not upload:
        return Response(
            {"detail": 'Missing file. Upload using multipart form field "file".'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    profile.profile_pic = upload.read()
    profile.profile_pic_mime = upload.content_type
    profile.save(update_fields=["profile_pic", "profile_pic_mime"])
    return Response({"detail": "Profile picture updated.", "profile_pic_mime": profile.profile_pic_mime})
