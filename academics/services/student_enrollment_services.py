from django.db import transaction, models
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from users.models import User
from academics.models import (
    Course, 
    Semester, 
    StudentEnrollment, 
    StudentLoadSemester,
    )


@transaction.atomic
def enroll_student_in_course(student: User, semester: Semester, course: Course) -> StudentEnrollment:
    """
    Enroll a student in a course for a specific semester,
    validating credit limits and preventing duplicates.

    Args:
        student (User): The student user instance.
        semester (Semester): The semester instance.
        course (Course): The course to enroll in.

    Returns:
        StudentEnrollment: The created enrollment instance.

    Raises:
        ValidationError: If the user is not a student, already enrolled,
                         lacks a semester load, or exceeds their credit limit.
    """
    if student.role != User.Role.STUDENT:
        raise ValidationError("Only users with the STUDENT role can enroll in courses.")

    try:
        student_load = StudentLoadSemester.objects.get(student=student, semester=semester)
    except ObjectDoesNotExist:
        raise ValidationError("Student has no configured semester load.")

    if StudentEnrollment.objects.filter(student=student, semester=semester, course=course).exists():
        raise ValidationError("Student is already enrolled in this course for the given semester.")

    current_credits = (
        StudentEnrollment.objects.filter(student=student, semester=semester)
        .select_related("course")
        .aggregate(total=models.Sum("course__credits"))["total"]
        or 0
    )

    if current_credits + course.credits > student_load.max_credits:
        raise ValidationError(
            f"Enrollment would exceed credit limit ({student_load.max_credits}). "
            f"Current: {current_credits}, New Course: {course.credits}."
        )

    enrollment = StudentEnrollment.objects.create(
        student=student,
        semester=semester,
        course=course
    )

    return enrollment
