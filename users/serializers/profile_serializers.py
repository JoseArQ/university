from rest_framework import serializers
from users.models import StudentProfile, TeacherProfile


class StudentProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = StudentProfile
        fields = [
            "user_id", 
            "username", 
            "email", 
            "enrollment_number", 
            "program",
            ]


class TeacherProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = TeacherProfile
        fields = [
            "user_id",
            "username", 
            "email", 
            "department",
            ]
