from django.urls import path
from accounts.views import RegisterView, LoginView, me, check_availability, send_test_email, request_password_reset, reset_password_confirm
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('availability/', check_availability, name='availability'),
    path('me/', me, name='me'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('email/test/', send_test_email, name='send_test_email'),
    path('password-reset/', request_password_reset, name='password_reset'),
    path('password-reset/confirm/', reset_password_confirm, name='password_reset_confirm'),
]
