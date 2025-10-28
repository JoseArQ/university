from rest_framework import serializers
from academics.models import StudentLoadSemester

class StudentLoadSemesterSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField(write_only=True)
    semester_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = StudentLoadSemester
        fields = [
            "id", 
            "student_id", 
            "semester_id", 
            "max_credits",
            ]

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "student": instance.student.username,
            "semester": str(instance.semester),
            "max_credits": instance.max_credits,
        }
