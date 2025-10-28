from django.db import transaction, models
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from academics.models import CourseOffering, Semester, Course, TeacherLoadSemester
from users.models import User

@transaction.atomic
def create_course_offering(teacher: User, semester: Semester, course: Course) -> CourseOffering:
    """
    Create a CourseOffering for a teacher in a given semester,
    ensuring the teacher does not exceed their maximum credit limit.

    Args:
        teacher (User): The teacher creating the offering.
        semester (Semester): The semester in which the course will be offered.
        course (Course): The course to offer.

    Returns:
        CourseOffering: The newly created offering.

    Raises:
        ValidationError: If the teacher has no credit limit configured,
                         exceeds available credits, or the offering already exists.
    """

    try:
        teacher_load = TeacherLoadSemester.objects.get(teacher=teacher, semester=semester)
    except ObjectDoesNotExist:
        raise ValidationError("Teacher has no configured credit limit for this semester.")

    if CourseOffering.objects.filter(teacher=teacher, semester=semester, course=course).exists():
        raise ValidationError("This course offering already exists for the given teacher and semester.")

    current_credits = (
        CourseOffering.objects.filter(teacher=teacher, semester=semester)
        .select_related("course")
        .aggregate(total=models.Sum("course__credits"))["total"]
        or 0
    )

    if current_credits + course.credits > teacher_load.max_credits:
        raise ValidationError(
            f"Teacher cannot exceed {teacher_load.max_credits} credits in semester "
            f"(current={current_credits}, new={course.credits})."
        )

    offering = CourseOffering.objects.create(
        teacher=teacher,
        semester=semester,
        course=course,
    )

    return offering
