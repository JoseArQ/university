from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist, ValidationError

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

def get_user_by_id(user_id: int) -> User:
    """
    Retrieve a user instance by its ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        User: The retrieved user instance.

    Raises:
        ValidationError: If the user_id is invalid or the user does not exist.
    """
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValidationError("Invalid user ID provided.")

    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        raise ValidationError(f"User with id={user_id} does not exist.")

    return user

# --- STUDENTS ---

def list_students() -> list[StudentProfile]:
    """
    Retrieve all student profiles.
    """
    return list(StudentProfile.objects.select_related("user").all())

# --- TEACHERS ---

def list_teachers() -> list[TeacherProfile]:
    """
    Retrieve all teacher profiles.
    """
    return list(TeacherProfile.objects.select_related("user").all())