from rest_framework import serializers
from academics.models import StudentEnrollment


class StudentEnrollmentCreateSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    semester_id = serializers.IntegerField()
    course_id = serializers.IntegerField()

    def to_representation(self, enrollment: StudentEnrollment):
        """Custom representation for API response."""
        return {
            "id": enrollment.id,
            "student": enrollment.student.username,
            "semester": str(enrollment.semester),
            "course": enrollment.course.name,
            "credits": enrollment.course.credits,
        }
