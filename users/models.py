from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STUDENT = "STUDENT", "Student"
        TEACHER = "TEACHER", "Teacher"

    role = models.CharField(
        max_length=50, 
        choices=Role.choices,
        default=Role.ADMIN
        )

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment_number = models.CharField(max_length=20)
    program = models.CharField(max_length=100)
    # semester = models.PositiveIntegerField()

    def __str__(self):
        return f"StudentProfile({self.user.username})"

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"TeacherProfile({self.user.username})"