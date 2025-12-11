from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User, UserActivity, Course, Subject, Question, Option
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
