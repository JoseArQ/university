from django.core.exceptions import ValidationError
from django.db import transaction

from academics.models import StudentLoadSemester, Semester
from users.models import User

@transaction.atomic
def assign_semester_to_student(student: User, semester: Semester, max_credits: int) -> StudentLoadSemester:
    """
    Assign a semester load to a student, defining their maximum allowed credits.

    Args:
        student (User): The student user instance.
        semester (Semester): The semester to assign.
        max_credits (int): Maximum credits allowed for the student in this semester.

    Returns:
        StudentLoadSemester: The created or updated semester load record.

    Raises:
        ValidationError: If the user is not a student or already has a load for the semester.
    """
    if student.role != User.Role.STUDENT:
        raise ValidationError("Only users with the STUDENT role can have semester loads assigned.")

    if max_credits <= 0:
        raise ValidationError("Max credits must be a positive integer.")

    if StudentLoadSemester.objects.filter(student=student, semester=semester).exists():
        raise ValidationError("This student already has a load assigned for the given semester.")

    student_semester = StudentLoadSemester.objects.create(
        student=student,
        semester=semester,
        max_credits=max_credits,
    )

    return student_semester
