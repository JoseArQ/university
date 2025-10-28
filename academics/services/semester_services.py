from django.core.exceptions import ValidationError, ObjectDoesNotExist

from academics.models import Semester

def create_semester(year: int, term: int) -> Semester:
    """
    Create a new academic semester if it does not already exist.

    Args:
        year (int): The year of the semester (e.g., 2025).
        term (int): The term number (1 for first, 2 for second).

    Returns:
        Semester: The created or existing Semester instance.

    Raises:
        ValidationError: If a semester with the same year and term already exists.
    """
    if Semester.objects.filter(year=year, term=term).exists():
        raise ValidationError(f"Semester {year}-{term} already exists.")

    semester = Semester.objects.create(year=year, term=term)
    return semester


def list_semesters() -> list[Semester]:
    """
    Retrieve all academic semesters ordered by year and term.

    Returns:
        list[Semester]: List of all semesters in chronological order.
    """
    return Semester.objects.all().order_by("year", "term")

def get_semester_by_id(semester_id: int) -> Semester:
    """
    Retrieve a Semester instance by its ID.

    Args:
        semester_id (int): The ID of the semester to retrieve.

    Returns:
        Semester: The retrieved Semester instance.

    Raises:
        ValidationError: If the semester_id is invalid or the semester does not exist.
    """
    if not isinstance(semester_id, int) or semester_id <= 0:
        raise ValidationError("Invalid semester ID provided.")

    try:
        semester = Semester.objects.get(id=semester_id)
    except ObjectDoesNotExist:
        raise ValidationError(f"Semester with id={semester_id} does not exist.")

    return semester