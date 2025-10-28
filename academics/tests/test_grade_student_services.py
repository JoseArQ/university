import pytest
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import IntegrityError

from academics.models import (
    Course,
    Semester,
    CourseOffering,
    StudentEnrollment,
)
from users.models import User
from academics.services.grade_student_services import grade_student_in_course
from academics.constants import MIN_GRADE, MAX_GRADE


@pytest.mark.django_db
class TestGradeStudentInCourse:
    @pytest.fixture
    def setup_data(self):
        # Users
        teacher = User.objects.create_user(username="teacher1", password="pass", role=User.Role.TEACHER)
        student = User.objects.create_user(username="student1", password="pass", role=User.Role.STUDENT)
        admin = User.objects.create_user(username="admin1", password="pass", role=User.Role.ADMIN)

        # Academic models
        semester = Semester.objects.create(year=2025, term=1)
        course = Course.objects.create(code="CS101", name="Intro to CS", credits=3)

        # Course offering (teacher teaches this course)
        CourseOffering.objects.create(teacher=teacher, semester=semester, course=course)

        # Enrollment (student is enrolled)
        enrollment = StudentEnrollment.objects.create(
            student=student,
            semester=semester,
            course=course
        )

        return {
            "teacher": teacher,
            "student": student,
            "admin": admin,
            "semester": semester,
            "course": course,
            "enrollment": enrollment,
        }

    def test_grade_student_success(self, setup_data):
        """✅ Teacher can successfully assign a valid grade to enrolled student."""
        data = setup_data
        enrollment = grade_student_in_course(
            teacher=data["teacher"],
            student=data["student"],
            semester=data["semester"],
            course=data["course"],
            grade=4.5,
        )

        assert enrollment.grade == 4.5
        enrollment.refresh_from_db()
        assert enrollment.grade == 4.5

    def test_invalid_teacher_role(self, setup_data):
        """❌ Only teachers can assign grades."""
        data = setup_data
        with pytest.raises(ValidationError, match="Only teachers can assign grades"):
            grade_student_in_course(
                teacher=data["admin"],
                student=data["student"],
                semester=data["semester"],
                course=data["course"],
                grade=4.0,
            )

    def test_invalid_grade_too_low(self, setup_data):
        """❌ Grade below MIN_GRADE should raise ValidationError."""
        data = setup_data
        with pytest.raises(ValidationError, match=f"Grade must be between {MIN_GRADE} and {MAX_GRADE}"):
            grade_student_in_course(
                teacher=data["teacher"],
                student=data["student"],
                semester=data["semester"],
                course=data["course"],
                grade=-1.0,
            )

    def test_invalid_grade_too_high(self, setup_data):
        """❌ Grade above MAX_GRADE should raise ValidationError."""
        data = setup_data
        with pytest.raises(ValidationError, match=f"Grade must be between {MIN_GRADE} and {MAX_GRADE}"):
            grade_student_in_course(
                teacher=data["teacher"],
                student=data["student"],
                semester=data["semester"],
                course=data["course"],
                grade=6.0,
            )

    def test_teacher_not_offering_course(self, setup_data):
        """❌ Teacher must be assigned to the course offering."""
        data = setup_data
        another_teacher = User.objects.create_user(username="teacher2", password="pass", role=User.Role.TEACHER)

        with pytest.raises(ValidationError, match="not authorized to grade this course"):
            grade_student_in_course(
                teacher=another_teacher,
                student=data["student"],
                semester=data["semester"],
                course=data["course"],
                grade=4.0,
            )

    def test_student_not_enrolled(self, setup_data):
        """❌ Cannot assign a grade if student is not enrolled in the course."""
        data = setup_data
        another_student = User.objects.create_user(username="student2", password="pass", role=User.Role.STUDENT)

        with pytest.raises(ValidationError, match="student is not enrolled"):
            grade_student_in_course(
                teacher=data["teacher"],
                student=another_student,
                semester=data["semester"],
                course=data["course"],
                grade=4.0,
            )
