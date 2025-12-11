from django.urls import path
from accounts.views import RegisterView, LoginView, me, check_availability, getCourseListBySubjectID, getCourseByCourseID, list_subjects
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('availability/', check_availability, name='availability'),
    path('me/', me, name='me'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('subjects/', list_subjects, name='subjects_list'),
    path('courses/subject/<int:subject_id>/', getCourseListBySubjectID, name='courses_by_subject'),
    path('courses/<int:course_id>/', getCourseByCourseID, name='course_detail'),
]
