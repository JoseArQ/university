import pytest
from django.core.exceptions import ValidationError

from academics.models import (
    Course,
    Semester,
    CourseOffering,
    TeacherLoadSemester,
)
from academics.services.course_offering_services import create_course_offering
from users.models import User


@pytest.mark.django_db
class TestCreateCourseOfferingService:

    @pytest.fixture
    def teacher(self, django_user_model):
        return django_user_model.objects.create_user(
            username="prof_john",
            email="prof.john@example.com",
            password="password123",
            role=User.Role.TEACHER,
        )

    @pytest.fixture
    def semester(self):
        return Semester.objects.create(year=2025, term=1)

    @pytest.fixture
    def courses(self):
        return [
            Course.objects.create(code="CS101", name="Intro to CS", credits=3),
            Course.objects.create(code="CS102", name="Algorithms", credits=4),
            Course.objects.create(code="CS103", name="AI Fundamentals", credits=2),
        ]

    def test_create_offering_success(self, teacher, semester, courses):
        """✅ Should create a course offering when the teacher has available credits."""
        TeacherLoadSemester.objects.create(teacher=teacher, semester=semester, max_credits=10)

        offering = create_course_offering(teacher=teacher, semester=semester, course=courses[0])

        assert offering.teacher == teacher
        assert offering.course == courses[0]
        assert offering.semester == semester
        assert CourseOffering.objects.count() == 1

    def test_create_offering_without_teacher_limit(self, teacher, semester, courses):
        """❌ Should raise ValidationError if teacher has no load configuration."""
        with pytest.raises(ValidationError, match="Teacher has no configured credit limit"):
            create_course_offering(teacher=teacher, semester=semester, course=courses[0])

    def test_create_offering_exceeds_credit_limit(self, teacher, semester, courses):
        """❌ Should raise ValidationError when teacher exceeds credit limit."""
        TeacherLoadSemester.objects.create(teacher=teacher, semester=semester, max_credits=6)

        # First offering: 4 credits
        create_course_offering(teacher=teacher, semester=semester, course=courses[1])

        # Second offering: +3 credits → exceeds 6
        with pytest.raises(ValidationError, match="Teacher cannot exceed"):
            create_course_offering(teacher=teacher, semester=semester, course=courses[0])

    def test_create_offering_duplicate(self, teacher, semester, courses):
        """❌ Should raise ValidationError if the same course offering already exists."""
        TeacherLoadSemester.objects.create(teacher=teacher, semester=semester, max_credits=12)

        create_course_offering(teacher=teacher, semester=semester, course=courses[0])

        with pytest.raises(ValidationError, match="This course offering already exists"):
            create_course_offering(teacher=teacher, semester=semester, course=courses[0])

    def test_create_multiple_offerings_within_limit(self, teacher, semester, courses):
        """✅ Should allow multiple offerings as long as total credits ≤ max_credits."""
        TeacherLoadSemester.objects.create(teacher=teacher, semester=semester, max_credits=9)

        create_course_offering(teacher=teacher, semester=semester, course=courses[0])  # 3 credits
        create_course_offering(teacher=teacher, semester=semester, course=courses[1])  # 4 credits
        create_course_offering(teacher=teacher, semester=semester, course=courses[2])  # 2 credits

        total_credits = sum(o.course.credits for o in CourseOffering.objects.filter(teacher=teacher))
        assert total_credits == 9
        assert CourseOffering.objects.count() == 3