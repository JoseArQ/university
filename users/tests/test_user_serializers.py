import pytest
from rest_framework.exceptions import ValidationError

from users.serializers.register_user_serializers import (
    BaseUserRegisterSerializer,
    StudentRegisterSerializer,
    TeacherRegisterSerializer,
)


@pytest.fixture
def mock_is_email_already_exists(monkeypatch):
    """Mockea la función user_services.is_email_already_exists."""
    def mock_func(email):
        return False
    monkeypatch.setattr("users.services.user_services.is_email_already_exists", mock_func)


@pytest.fixture
def mock_is_email_taken(monkeypatch):
    """Mockea para simular que el email ya existe."""
    def mock_func(email):
        return True
    monkeypatch.setattr("users.services.user_services.is_email_already_exists", mock_func)


# ---------------------------------------------------------------------
# BaseUserRegisterSerializer
# ---------------------------------------------------------------------

def test_base_user_serializer_valid_data(mock_is_email_already_exists):
    data = {
        "username": "johndoe",
        "email": "John@Example.com",
        "password": "securePass123",
    }
    serializer = BaseUserRegisterSerializer(data=data)
    assert serializer.is_valid(), serializer.errors

    validated = serializer.validated_data
    assert validated["email"] == "john@example.com"  # Debe quedar en minúsculas
    assert validated["username"] == "johndoe"


def test_base_user_serializer_duplicate_email(mock_is_email_taken):
    data = {
        "username": "johndoe",
        "email": "john@example.com",
        "password": "securePass123",
    }
    serializer = BaseUserRegisterSerializer(data=data)
    with pytest.raises(ValidationError) as exc:
        serializer.is_valid(raise_exception=True)
    assert "A user with this email already exists." in str(exc.value)


def test_base_user_serializer_short_password(mock_is_email_already_exists):
    data = {
        "username": "johndoe",
        "email": "john@example.com",
        "password": "123",
    }
    serializer = BaseUserRegisterSerializer(data=data)
    assert not serializer.is_valid()
    assert "password" in serializer.errors


# ---------------------------------------------------------------------
# StudentRegisterSerializer
# ---------------------------------------------------------------------

def test_student_serializer_requires_fields(mock_is_email_already_exists):
    """Debe exigir enrollment_number y program."""
    data = {
        "username": "student1",
        "email": "student@example.com",
        "password": "securePass123",
    }
    serializer = StudentRegisterSerializer(data=data)
    assert not serializer.is_valid()
    assert "enrollment_number" in serializer.errors
    assert "program" in serializer.errors


def test_student_serializer_valid_data(mock_is_email_already_exists):
    data = {
        "username": "student1",
        "email": "student@example.com",
        "password": "securePass123",
        "enrollment_number": "A12345",
        "program": "Computer Science",
    }
    serializer = StudentRegisterSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    validated = serializer.validated_data
    assert validated["enrollment_number"] == "A12345"
    assert validated["program"] == "Computer Science"


# ---------------------------------------------------------------------
# TeacherRegisterSerializer
# ---------------------------------------------------------------------

def test_teacher_serializer_requires_department(mock_is_email_already_exists):
    data = {
        "username": "teacher1",
        "email": "teacher@example.com",
        "password": "securePass123",
    }
    serializer = TeacherRegisterSerializer(data=data)
    assert not serializer.is_valid()
    assert "department" in serializer.errors


def test_teacher_serializer_valid_data(mock_is_email_already_exists):
    data = {
        "username": "teacher1",
        "email": "teacher@example.com",
        "password": "securePass123",
        "department": "Mathematics",
    }
    serializer = TeacherRegisterSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    validated = serializer.validated_data
    assert validated["department"] == "Mathematics"
