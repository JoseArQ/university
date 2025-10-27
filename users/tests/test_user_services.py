import pytest

from django.db import IntegrityError
from django.contrib.auth import get_user_model

from users.models import StudentProfile, TeacherProfile  
from users.services import user_services

User = get_user_model()


@pytest.mark.django_db
class TestCreateUserStudent:
    def test_create_student_user_success(self):
        """Should create a student user and associated profile."""
        user = user_services.create_user_student(
            username="john_doe",
            email="john@example.com",
            password="securepass123",
            enrollment_number="A12345",
            program="Computer Science",
        )

        assert user.username == "john_doe"
        assert user.email == "john@example.com"
        assert user.role == User.Role.STUDENT
        assert user.check_password("securepass123")

        profile = StudentProfile.objects.get(user=user)
        assert profile.enrollment_number == "A12345"
        assert profile.program == "Computer Science"

    def test_email_is_lowercased(self):
        """Should lowercase the email when creating a student user."""
        user = user_services.create_user_student(
            username="alice",
            email="Alice@Example.COM",
            password="password123",
        )
        assert user.email == "alice@example.com"

    def test_raises_error_when_no_email(self):
        """Should raise ValueError if email is not provided."""
        with pytest.raises(ValueError, match="Email is required for student users."):
            user_services.create_user_student(username="noemail", email="", password="pass123")

    def test_atomic_transaction_rolls_back_on_profile_error(self):
        """If profile creation fails, user creation must be rolled back."""
        # Forzamos un fallo en el perfil (por ejemplo, campo requerido faltante)
        with pytest.raises(IntegrityError):
            user_services.create_user_student(
                username="fail_user",
                email="fail@example.com",
                password="pass123",
                enrollment_number=None,  # Asumimos que este campo es required
            )

        # Verifica que no se creó el usuario
        assert not User.objects.filter(username="fail_user").exists()

@pytest.mark.django_db
class TestCreateUserTeacher:
    def test_create_teacher_user_success(self):
        """Should create a teacher user and associated profile."""
        user = user_services.create_user_teacher(
            username="prof_smith",
            email="smith@example.com",
            password="teachpass123",
            department="Mathematics",
        )

        # Verifica que se creó el usuario correctamente
        assert user.username == "prof_smith"
        assert user.email == "smith@example.com"
        assert user.role == User.Role.TEACHER
        assert user.check_password("teachpass123")

        # Verifica que se creó el perfil asociado
        profile = TeacherProfile.objects.get(user=user)
        assert profile.department == "Mathematics"

    def test_email_is_lowercased(self):
        """Should lowercase the email when creating a teacher user."""
        user = user_services.create_user_teacher(
            username="teacher_x",
            email="TEACHER@Example.COM",
            password="password123",
        )
        assert user.email == "teacher@example.com"

    def test_raises_error_when_no_email(self):
        """Should raise ValueError if email is not provided."""
        with pytest.raises(ValueError, match="Email is required for teacher users."):
            user_services.create_user_teacher(username="noemail", email="", password="pass123")

    def test_atomic_transaction_rolls_back_on_profile_error(self):
        """If profile creation fails, user creation must be rolled back."""
        with pytest.raises(IntegrityError):
            user_services.create_user_teacher(
                username="broken_teacher",
                email="broken@example.com",
                password="pass123",
                department=None,  
            )

        assert not User.objects.filter(username="broken_teacher").exists()