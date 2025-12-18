import secrets
from datetime import date, timedelta

from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
<<<<<<< HEAD
from accounts.models import User, UserActivity, Course, Subject, Question, Option, UserCourse
from accounts.serializers import (
    UserSerializer,
    CourseSerializer,
    SubjectSerializer,
    QuestionSerializer,
    QuestionDetailSerializer,
)
from datetime import date, timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
=======

from accounts.models import PasswordResetToken, User, UserActivity
from accounts.serializers import UserSerializer
>>>>>>> 2ff884d (add password reset via email token)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
def check_availability(request):
    user_name = request.query_params.get('user_name')
    email = request.query_params.get('email')

    if not user_name and not email:
        return Response(
            {"detail": "Provide at least one of user_name or email query params."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    data = {}
    if user_name:
        data['user_name_available'] = not User.objects.filter(user_name=user_name).exists()
    if email:
        data['email_available'] = not User.objects.filter(email=email).exists()

    return Response(data)


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Log registration activity
        UserActivity.objects.create(user=user, activity_type='REGISTRATION')
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        user_name = request.data.get('user_name')
        password = request.data.get('password')
        try:
            user = User.objects.get(user_name=user_name)
            if user.check_password(password):
                # Update login streak
                self.update_login_streak(user)
                # Log login activity
                UserActivity.objects.create(user=user, activity_type='LOGIN')
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data,  # Include user data
                })
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    def update_login_streak(self, user):
        profile = user.profile
        today = date.today()
        if profile.last_login_date:
            if profile.last_login_date == today:
                # Already logged in today, do nothing
                pass
            elif profile.last_login_date == today - timedelta(days=1):
                # Logged in yesterday, increment streak
                profile.login_streak_days += 1
            else:
                # Skipped a day or more, reset streak
                profile.login_streak_days = 1
        else:
            # First login
            profile.login_streak_days = 1
        profile.last_login_date = today
        profile.save()


<<<<<<< HEAD
@api_view(['GET'])
def getCourseListBySubjectID(request, subject_id):
    courses = Course.objects.filter(SubjectID_id=subject_id).only('CourseID', 'CourseTitle')
    serializer = CourseSerializer(courses, many=True)
    # Only return ID and name as requested
    data = [
        {
            'CourseID': item['CourseID'],
            'CourseTitle': item['CourseTitle'],
        }
        for item in serializer.data
    ]
    return Response(data)


@api_view(['GET'])
def getCourseByCourseID(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return Response({'detail': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CourseSerializer(course)
    return Response(serializer.data)


@api_view(['GET'])
def list_subjects(request):
    subjects = Subject.objects.all()
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getQuestionListByCourseID(request, course_id):
    questions = Question.objects.filter(CourseID_id=course_id).only('QuestionID')
    serializer = QuestionSerializer(questions, many=True)
    # Only return question IDs as requested
    data = [item['QuestionID'] for item in serializer.data]
    return Response(data)


@api_view(['GET'])
def getQuestionByQuestionID(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return Response({'detail': 'Question not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = QuestionDetailSerializer(question)
    return Response(serializer.data)


@api_view(['GET'])
def verifyAnsByOptionID(request, option_id):
    """Return whether the given option is correct.

    Response shape: { "correct": true/false }
    """
    try:
        option = Option.objects.get(pk=option_id)
    except Option.DoesNotExist:
        return Response({'detail': 'Option not found.'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'correct': bool(option.CorrectOption)})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def markCourseCompletedByCourseID(request, course_id):
    """Mark a course as completed for the current user and update score if higher.

    Expects JSON body: { "score": <number> }
    """
    score = request.data.get('score')
    if score is None:
        return Response({'detail': 'score is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        new_score_int = int(score)
    except (TypeError, ValueError):
        return Response({'detail': 'score must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)

    user = request.user

    # Ensure the course exists (optional but clearer error)
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return Response({'detail': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)

    user_course, created = UserCourse.objects.get_or_create(
        CourseID=course,
        UserID=user,
        defaults={
            'CourseScore': str(new_score_int),
            'CourseFlag': 'completed',
        },
    )

    if not created:
        # Update score only if the new score is higher
        try:
            existing_score_int = int(user_course.CourseScore)
        except (TypeError, ValueError):
            existing_score_int = 0

        if new_score_int > existing_score_int:
            user_course.CourseScore = str(new_score_int)

        user_course.CourseFlag = 'completed'
        user_course.save()

    return Response(
        {
            'CourseID': course.CourseID,
            'CourseFlag': user_course.CourseFlag,
            'CourseScore': user_course.CourseScore,
        }
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCompletedCourse(request):
    """Return list of course IDs where CourseFlag is 'completed' for current user."""
    user = request.user
    completed = UserCourse.objects.filter(UserID=user, CourseFlag='completed').values_list('CourseID_id', flat=True)
    # Cast to list of integers for JSON response
    return Response(list(completed))
=======
@api_view(['POST'])
def send_test_email(request):
    recipient = request.data.get('to')
    subject = request.data.get('subject', 'CSCI3100 Notification')
    message = request.data.get('message', 'This is a test email from the CSCI3100 backend.')

    if not recipient:
        return Response({'detail': 'Missing "to" email address.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
    except BadHeaderError:
        return Response({'detail': 'Invalid header found.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as exc:
        return Response({'detail': f'Failed to send email: {exc}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'detail': f'Email sent to {recipient}.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def request_password_reset(request):
    email = request.data.get('email')
    reset_base_url = request.data.get('reset_base_url') or settings.RESET_PASSWORD_FRONTEND_URL

    if not email:
        return Response({'detail': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(email=email).first()

    if user:
        token = secrets.token_urlsafe(48)
        expires_at = timezone.now() + timedelta(hours=1)
        PasswordResetToken.objects.create(user=user, token=token, expires_at=expires_at)

        reset_link = f"{reset_base_url}?token={token}&email={email}"
        subject = 'CSCI3100 Password Reset'
        message = (
            f"Hi {user.user_name},\n\n"
            f"This is a mock password reset email. Click the link below to reset your password:\n"
            f"{reset_link}\n\n"
            f"If you did not request this, you can ignore this email.\n\n"
            f"- CSCI3100 Team"
        )

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except BadHeaderError:
            return Response({'detail': 'Invalid header found.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            return Response({'detail': f'Failed to send email: {exc}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'detail': 'If an account exists for that email, you will receive reset instructions shortly.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def reset_password_confirm(request):
    token = request.data.get('token')
    email = request.data.get('email')
    new_password = request.data.get('new_password')

    if not token or not email or not new_password:
        return Response({'detail': 'token, email, and new_password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    token_obj = PasswordResetToken.objects.filter(token=token, used=False).select_related('user').first()
    if (
        not token_obj
        or token_obj.user.email.lower() != email.lower()
        or timezone.now() > token_obj.expires_at
    ):
        return Response({'detail': 'Invalid or expired reset token.'}, status=status.HTTP_400_BAD_REQUEST)

    user = token_obj.user
    if len(new_password) < 8:
        return Response({'detail': 'Password must be at least 8 characters long.'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()
    token_obj.used = True
    token_obj.save(update_fields=['used'])

    UserActivity.objects.create(user=user, activity_type='LOGIN', details='Password reset (mock)')

    return Response({'detail': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
>>>>>>> 2ff884d (add password reset via email token)
