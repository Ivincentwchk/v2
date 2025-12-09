from django.urls import path
from accounts.views import RegisterView, LoginView, me, check_availability
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('availability/', check_availability, name='availability'),
    path('me/', me, name='me'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
