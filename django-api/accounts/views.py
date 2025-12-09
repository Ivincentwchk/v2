from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User, UserActivity
from accounts.serializers import UserSerializer
from datetime import date, timedelta
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


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
