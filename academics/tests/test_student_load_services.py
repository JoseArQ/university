import pytest
from django.core.exceptions import ValidationError

from academics.models import Semester, StudentLoadSemester
from academics.services.student_load_services import assign_semester_to_student
from users.models import User


@pytest.mark.django_db
class TestAssignSemesterToStudent:
    def test_assign_semester_successfully(self):
        """
        ✅ Debe crear correctamente una carga académica para un estudiante válido.
        """
        student = User.objects.create_user(
            username="student1",
            email="student1@example.com",
            password="pass123",
            role=User.Role.STUDENT,
        )
        semester = Semester.objects.create(year=2025, term=1)

        load = assign_semester_to_student(student=student, semester=semester, max_credits=18)

        assert isinstance(load, StudentLoadSemester)
        assert load.student == student
        assert load.semester == semester
        assert load.max_credits == 18
        assert StudentLoadSemester.objects.count() == 1

    def test_assign_semester_duplicate_fails(self):
        """
        🚫 Debe fallar si el estudiante ya tiene un semestre asignado.
        """
        student = User.objects.create_user(
            username="student2",
            email="student2@example.com",
            password="pass123",
            role=User.Role.STUDENT,
        )
        semester = Semester.objects.create(year=2025, term=1)

        StudentLoadSemester.objects.create(student=student, semester=semester, max_credits=15)

        with pytest.raises(ValidationError, match="already has a load assigned"):
            assign_semester_to_student(student=student, semester=semester, max_credits=20)

    def test_assign_semester_invalid_role_fails(self):
        """
        🚫 Debe fallar si el usuario no tiene rol de estudiante.
        """
        teacher = User.objects.create_user(
            username="teacher1",
            email="teacher@example.com",
            password="pass123",
            role=User.Role.TEACHER,
        )
        semester = Semester.objects.create(year=2025, term=1)

        with pytest.raises(ValidationError, match="Only users with the STUDENT role"):
            assign_semester_to_student(student=teacher, semester=semester, max_credits=20)

    def test_assign_semester_invalid_max_credits_fails(self):
        """
        🚫 Debe fallar si los créditos son menores o iguales a cero.
        """
        student = User.objects.create_user(
            username="student3",
            email="student3@example.com",
            password="pass123",
            role=User.Role.STUDENT,
        )
        semester = Semester.objects.create(year=2025, term=1)

        with pytest.raises(ValidationError, match="Max credits must be a positive integer"):
            assign_semester_to_student(student=student, semester=semester, max_credits=0)

    def test_assign_semester_is_atomic(self, db):
        """
        ✅ Debe garantizar atomicidad (no se crea registro si ocurre error).
        """
        student = User.objects.create_user(
            username="student4",
            email="student4@example.com",
            password="pass123",
            role=User.Role.STUDENT,
        )
        semester = Semester.objects.create(year=2025, term=1)
        StudentLoadSemester.objects.create(student=student, semester=semester, max_credits=10)

        # Debe lanzar error y no crear registro parcial
        with pytest.raises(ValidationError):
            assign_semester_to_student(student=student, semester=semester, max_credits=12)

        assert StudentLoadSemester.objects.count() == 1
