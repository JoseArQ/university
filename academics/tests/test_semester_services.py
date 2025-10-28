import pytest
from django.core.exceptions import ValidationError

from academics.models import Semester
from academics.services import semester_services


@pytest.mark.django_db
class TestSemesterServices:
    def test_create_semester_success(self):
        """Should create a new semester when it does not exist."""
        semester = semester_services.create_semester(year=2025, term=1)

        assert semester.year == 2025
        assert semester.term == 1
        assert Semester.objects.count() == 1
        assert str(semester) == "2025-1"

    def test_create_semester_duplicate_raises_error(self):
        """Should raise ValidationError if the semester already exists."""
        Semester.objects.create(year=2025, term=1)

        with pytest.raises(ValidationError, match="Semester 2025-1 already exists."):
            semester_services.create_semester(year=2025, term=1)

        # Should not create a new record
        assert Semester.objects.count() == 1

    def test_list_semesters_returns_ordered_list(self):
        """Should return all semesters ordered by year and term."""
        Semester.objects.create(year=2024, term=2)
        Semester.objects.create(year=2023, term=1)
        Semester.objects.create(year=2025, term=1)

        semesters = semester_services.list_semesters()

        assert [s.year for s in semesters] == [2023, 2024, 2025]
        assert semesters[0].term == 1  # 2023-1
        assert len(semesters) == 3
