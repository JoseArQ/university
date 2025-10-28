from django.db import transaction
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from ..constants import MAX_GRADE, MIN_GRADE

from users.models import User
from academics.models import Semester, Course, StudentEnrollment, CourseOffering

@transaction.atomic
def grade_student_in_course(
    teacher: User, 
    student: User, 
    semester: Semester, 
    course: Course, 
    grade: float) -> StudentEnrollment:
    """
    Assign a grade to a student in a specific course and semester, ensuring
    that the teacher is authorized to teach that course.

    Args:
        teacher (User): The teacher assigning the grade.
        student (User): The student receiving the grade.
        semester (Semester): The academic semester of the enrollment.
        course (Course): The course being graded.
        grade (float): The grade value (between 0.0 and 5.0).

    Returns:
        StudentEnrollment: The updated enrollment record with the assigned grade.

    Raises:
        ValidationError: If:
            - The user is not a teacher.
            - The teacher is not assigned to the course offering.
            - The student is not enrolled in the course.
            - The grade is outside the valid range (0.0–5.0).
    """

    if teacher.role != teacher.Role.TEACHER:
        raise ValidationError("Only teachers can assign grades.")

    if not (MIN_GRADE <= grade <= MAX_GRADE):
        raise ValidationError(f"Grade must be between {MIN_GRADE} and {MAX_GRADE}.")

    if not CourseOffering.objects.filter(
        teacher=teacher, semester=semester, course=course
    ).exists():
        raise ValidationError("You are not authorized to grade this course.")

    try:
        enrollment = StudentEnrollment.objects.get(
            student=student, semester=semester, course=course
        )
    except ObjectDoesNotExist:
        raise ValidationError("The student is not enrolled in this course.")

    enrollment.grade = grade
    enrollment.full_clean()
    enrollment.save()

    return enrollment