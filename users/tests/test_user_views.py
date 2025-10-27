import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from unittest.mock import patch
from users.models import User


@pytest.mark.django_db
class TestStudentRegisterView:
    """Tests for StudentRegisterView."""

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def valid_payload(self):
        return {
            "username": "john_doe",
            "email": "john@example.com",
            "password": "StrongPass123",
            "enrollment_number": "ENR2025",
            "program": "Computer Science",
        }

    def test_student_register_success(self, client, valid_payload):
        """Should return 201 and create student user."""
        url = reverse("register-student")

        # Mock the service to return a fake user
        mock_user = User(id=1, role=User.Role.STUDENT)
        with patch("users.services.user_services.create_user_student", return_value=mock_user):
            response = client.post(url, valid_payload, format="json")

        assert response.status_code == 201
        assert response.data["is_ok"] is True
        assert response.data["data"]["role"] == User.Role.STUDENT

    def test_student_register_invalid_data(self, client):
        """Should return 400 when missing required fields."""
        url = reverse("register-student")
        invalid_payload = {"username": "no_email"}  # Missing email, password, etc.
        response = client.post(url, invalid_payload, format="json")

        assert response.status_code == 400
        assert response.data["is_ok"] is False
        assert "email" in response.data["errors"]


@pytest.mark.django_db
class TestTeacherRegisterView:
    """Tests for TeacherRegisterView."""

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def valid_payload(self):
        return {
            "username": "prof_smith",
            "email": "smith@example.com",
            "password": "StrongPass123",
            "department": "Physics",
        }

    def test_teacher_register_success(self, client, valid_payload):
        """Should return 201 and create teacher user."""
        url = reverse("register-teacher")

        # Mock the service to avoid real DB write
        mock_user = User(id=2, role=User.Role.TEACHER)
        with patch("users.services.user_services.create_user_teacher", return_value=mock_user):
            response = client.post(url, valid_payload, format="json")

        assert response.status_code == 201
        assert response.data["is_ok"] is True
        assert response.data["data"]["role"] == User.Role.TEACHER

    def test_teacher_register_missing_field(self, client):
        """Should return 400 when missing department."""
        url = reverse("register-teacher")
        invalid_payload = {
            "username": "prof_smith",
            "email": "smith@example.com",
            "password": "StrongPass123",
            # Missing department
        }

        response = client.post(url, invalid_payload, format="json")

        assert response.status_code == 400
        assert response.data["is_ok"] is False
        assert "department" in response.data["errors"]
