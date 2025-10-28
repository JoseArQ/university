from django.db import transaction
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from academics.models import Semester, TeacherLoadSemester

from users.models import User

@transaction.atomic
def assign_semester_to_teacher(teacher: User, semester: Semester, max_credits: int) -> TeacherLoadSemester:
    """
    Assign a semester load to a teacher with a maximum credit limit.

    Args:
        teacher (User): Teacher user instance.
        semester (Semester): Semester instance.
        max_credits (int): Maximum credits the teacher can handle.

    Returns:
        TeacherLoadSemester: The created TeacherLoadSemester instance.

    Raises:
        ValidationError: If the teacher already has a load assigned for the semester.
    """
    if not teacher or teacher.role != User.Role.TEACHER:
        raise ValidationError("The provided user is not a teacher.")

    if TeacherLoadSemester.objects.filter(teacher=teacher, semester=semester).exists():
        raise ValidationError(f"Teacher {teacher.username} already has a load for {semester}.")

    if max_credits <= 0:
        raise ValidationError("max_credits must be greater than 0.")

    teacher_load = TeacherLoadSemester.objects.create(
        teacher=teacher,
        semester=semester,
        max_credits=max_credits,
    )
    return teacher_load


def get_teacher_max_credits(teacher: User, semester: Semester) -> int:
    """
    Retrieve the maximum credits a teacher can handle for a given semester.

    Args:
        teacher (User): Teacher user instance.
        semester (Semester): Semester instance.

    Returns:
        int: The maximum credits for the teacher in the semester.

    Raises:
        ObjectDoesNotExist: If the teacher has no load assigned for that semester.
    """
    try:
        teacher_load = TeacherLoadSemester.objects.get(
            teacher=teacher, 
            semester=semester,
            )
        return teacher_load.max_credits
    except TeacherLoadSemester.DoesNotExist:
        raise ObjectDoesNotExist(f"No load found for teacher {teacher.username} in semester {semester}.")
