from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..services import user_services

User = get_user_model()

class BaseUserRegisterSerializer(serializers.Serializer):
    """
    Base serializer for user registration.
    Contains shared fields for all roles.
    """
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_email(self, value):
        """Ensure the email is unique (case-insensitive)."""
        if user_services.is_email_already_exists(email=value):
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()


class StudentRegisterSerializer(BaseUserRegisterSerializer):
    """
    Serializer for registering student users.
    """
    enrollment_number = serializers.CharField(max_length=50)
    program = serializers.CharField(max_length=100)


class TeacherRegisterSerializer(BaseUserRegisterSerializer):
    """
    Serializer for registering teacher users.
    """
    department = serializers.CharField(max_length=100)
