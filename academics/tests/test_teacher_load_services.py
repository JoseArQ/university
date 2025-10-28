import pytest
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from academics.models import TeacherLoadSemester, Semester
from academics.services import teacher_load_services
from users.models import User


@pytest.mark.django_db
class TestTeacherLoadServices:

    @pytest.fixture
    def teacher_user(self):
        return User.objects.create_user(
            username="teacher1",
            email="teacher1@example.com",
            password="password123",
            role=User.Role.TEACHER,
        )

    @pytest.fixture
    def student_user(self):
        return User.objects.create_user(
            username="student1",
            email="student1@example.com",
            password="password123",
            role=User.Role.STUDENT,
        )

    @pytest.fixture
    def semester(self):
        return Semester.objects.create(year=2025, term=1)

    def test_assign_semester_to_teacher_success(self, teacher_user, semester):
        load = teacher_load_services.assign_semester_to_teacher(
            teacher=teacher_user, semester=semester, max_credits=12
        )

        assert load.teacher == teacher_user
        assert load.semester == semester
        assert load.max_credits == 12
        assert TeacherLoadSemester.objects.count() == 1

    def test_assign_semester_to_teacher_fails_if_not_teacher(self, student_user, semester):
        with pytest.raises(ValidationError, match="not a teacher"):
            teacher_load_services.assign_semester_to_teacher(
                teacher=student_user, semester=semester, max_credits=10
            )

    def test_assign_semester_to_teacher_fails_if_duplicate(self, teacher_user, semester):
        teacher_load_services.assign_semester_to_teacher(
            teacher=teacher_user, semester=semester, max_credits=10
        )

        with pytest.raises(ValidationError, match="already has a load"):
            teacher_load_services.assign_semester_to_teacher(
                teacher=teacher_user, semester=semester, max_credits=12
            )

    def test_assign_semester_to_teacher_fails_if_invalid_max_credits(self, teacher_user, semester):
        with pytest.raises(ValidationError, match="greater than 0"):
            teacher_load_services.assign_semester_to_teacher(
                teacher=teacher_user, semester=semester, max_credits=0
            )

    def test_get_teacher_max_credits_success(self, teacher_user, semester):
        teacher_load_services.assign_semester_to_teacher(
            teacher=teacher_user, semester=semester, max_credits=15
        )

        result = teacher_load_services.get_teacher_max_credits(teacher_user, semester)
        assert result == 15

    def test_get_teacher_max_credits_not_found(self, teacher_user, semester):
        with pytest.raises(ObjectDoesNotExist, match="No load found"):
            teacher_load_services.get_teacher_max_credits(teacher_user, semester)
