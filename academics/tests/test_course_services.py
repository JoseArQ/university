import pytest
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from academics.models import Course, Semester
from academics.models.course_offering import CourseOffering

from academics.services import course_services


@pytest.mark.django_db
class TestCourseServices:

    def test_create_course_success(self):
        course = course_services.create_course(
            code="CS101",
            name="Intro to Programming",
            credits=3
        )
        assert course.id is not None
        assert course.code == "CS101"
        assert course.credits == 3
        assert course.prerequisites.count() == 0

    def test_create_course_with_prerequisite(self):
        prereq = Course.objects.create(
            code="CS100", 
            name="Basic Computing", 
            credits=2,
            )
        
        course = course_services.create_course(
            code="CS200",
            name="Data Structures",
            credits=4,
            prerequisites=[prereq]
        )
        assert prereq in course.prerequisites.all()
        assert course.prerequisites.count() == 1

    def test_create_course_invalid_credits(self):
        with pytest.raises(ValidationError) as excinfo:
            course_services.create_course(
                code="CS001",
                name="Invalid Course",
                credits=0
            )
        assert "Credits must be greater than zero" in str(excinfo.value)

    def test_create_course_self_prerequisite_fails(self):
        course = Course(code="CS999", name="Self Ref", credits=3)
        course.save()

        with pytest.raises(ValidationError) as excinfo:
            course_services.create_course(
                code="CS998",
                name="Depends on self",
                credits=3,
                prerequisites=[course]
            )
        assert "A course cannot be its own prerequisite" in str(excinfo.value)

    def test_get_course_by_id_success(self):
        course = Course.objects.create(
            code="CS150", name="Algorithms", credits=3)
        found = course_services.get_course_by_id(course.id)
        assert found == course

    def test_get_course_by_id_not_found(self):
        with pytest.raises(ObjectDoesNotExist):
            course_services.get_course_by_id(999)

    def test_get_course_by_code_success(self):
        course = Course.objects.create(
            code="CS300", name="Operating Systems", credits=4)
        found = course_services.get_course_by_code("CS300")
        assert found == course

    def test_get_course_by_code_not_found(self):
        with pytest.raises(ObjectDoesNotExist):
            course_services.get_course_by_code("NOPE")

    def test_get_all_courses(self):
        Course.objects.create(code="C1", name="Math", credits=2)
        Course.objects.create(code="C2", name="Science", credits=3)
        all_courses = course_services.get_all_courses()
        assert len(all_courses) == 2
        assert all(isinstance(c, Course) for c in all_courses)

    def test_get_courses_by_semester(self):
        semester = Semester.objects.create(year=2025, term=1)
        course1 = Course.objects.create(code="CS400", name="Networks", credits=3)
        course2 = Course.objects.create(code="CS401", name="AI", credits=4)
        
        CourseOffering.objects.create(course=course1, semester=semester)
        CourseOffering.objects.create(course=course2, semester=semester)

        courses = course_services.get_courses_by_semester(semester)
        assert len(courses) == 2
        assert course1 in courses and course2 in courses
