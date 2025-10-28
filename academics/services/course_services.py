from django.core.exceptions import ValidationError, ObjectDoesNotExist
from academics.models import Course, Semester

def create_course(code: str, name: str, credits: int, prerequisites=None) -> Course:
    """
    Create a new course with optional prerequisites.
    Ensures prerequisites are valid and no cyclic dependencies exist.
    """
    if credits <= 0:
        raise ValidationError("Credits must be greater than zero.")

    prerequisites = prerequisites or []

    course = Course.objects.create(code=code, name=name, credits=credits)

    for prereq in prerequisites:
        if prereq == course:
            raise ValidationError("A course cannot be its own prerequisite.")
        course.prerequisites.add(prereq)

    course.full_clean()
    course.save()
    return course


def get_course_by_id(course_id: int) -> Course:
    """
    Retrieve a course by its database ID.
    """
    try:
        return Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        raise ObjectDoesNotExist(f"No course found with ID {course_id}.")


def get_course_by_code(code: str) -> Course:
    """
    Retrieve a course by its unique code.
    """
    try:
        return Course.objects.get(code=code)
    except Course.DoesNotExist:
        raise ObjectDoesNotExist(f"No course found with code '{code}'.")


def get_all_courses() -> list[Course]:
    """
    Retrieve all courses available in the system.
    """
    return list(Course.objects.all())


def get_courses_by_semester(semester: Semester) -> list[Course]:
    """
    Retrieve courses offered in a specific semester.
    Assumes a relationship exists between Course and Semester (e.g., CourseOffering).
    """
    return list(
        Course.objects.filter(
            offerings__semester=semester,
            ).distinct()
        )

def get_courses_by_ids(course_ids: list[int]) -> list[Course]:
    """
    Retrieve a list of Course instances given a list of IDs.

    Args:
        course_ids (list[int]): List of course IDs.

    Returns:
        list[Course]: List of Course objects matching the provided IDs.

    Raises:
        ValidationError: If any provided ID does not correspond to an existing Course.
    """
    if not course_ids:
        return []

    courses = list(Course.objects.filter(id__in=course_ids))

    missing_ids = set(course_ids) - {course.id for course in courses}
    if missing_ids:
        raise ValidationError(f"Courses not found for IDs: {missing_ids}")

    return courses