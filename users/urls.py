from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views.user_register_views import StudentRegisterView, TeacherRegisterView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("register/student/", StudentRegisterView.as_view(), name="register-student"),
    path("register/teacher/", TeacherRegisterView.as_view(), name="register-teacher"),
]
