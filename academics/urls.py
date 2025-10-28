from django.urls import path
from academics.views.semester_views import SemesterView
from academics.views.teacher_load_views import TeacherLoadAssignView
from academics.views.course_views import CourseView
from academics.views.course_offering_views import CourseOfferingCreateView
from academics.views.student_load_views import AssignSemesterToStudentView
from academics.views.student_enrollment_views import StudentEnrollmentView

urlpatterns = [
    path("semesters/", SemesterView.as_view(), name="semesters"),
    path("teacher-load/assign/", TeacherLoadAssignView.as_view(), name="teacher-assign"),
    path("courses/", CourseView.as_view(), name="courses"),
    path("courses-offering/", CourseOfferingCreateView.as_view(), name="courses-offering"),
    path("student-semesters/", AssignSemesterToStudentView.as_view(), name="assign-student-semester"),
    path("enrollments/", StudentEnrollmentView.as_view(), name="student-enroll"),
]