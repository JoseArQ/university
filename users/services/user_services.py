from django.db import transaction

from ..models import User, StudentProfile, TeacherProfile

@transaction.atomic
def create_user_student(username: str, email: str, password: str, **profile_data) -> User:
    """
    Create a student user with a securely hashed password and STUDENT role.

    Args:
        username (str): Username for the student.
        email (str): Email address for the student.
        password (str): Plain text password.

    Returns:
        User: Created User instance with STUDENT role.
    """
    if not email:
        raise ValueError("Email is required for student users.")

    user = User.objects.create_user(
        username=username, 
        email=email.lower(), 
        password=password, 
        role=User.Role.STUDENT,
        )
    StudentProfile.objects.create(user=user, **profile_data)
    return user

@transaction.atomic
def create_user_teacher(username: str, email: str, password: str, **profile_data) -> User:
    """
    Create a teacher user with a securely hashed password and TEACHER role.

    Args:
        username (str): Username for the teacher.
        email (str): Email address for the teacher.
        password (str): Plain text password.

    Returns:
        User: Created User instance with TEACHER role.
    """
    if not email:
        raise ValueError("Email is required for teacher users.")

    user = User.objects.create_user(
        username=username, 
        email=email.lower(), 
        password=password, 
        role=User.Role.TEACHER,
        )
    TeacherProfile.objects.create(user=user, **profile_data)
    return user

def is_email_already_exists(email : str) -> bool:
    return User.objects.filter(email__iexact=email).exists()