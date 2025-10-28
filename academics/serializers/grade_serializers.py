from rest_framework import serializers

from academics.constants import MIN_GRADE, MAX_GRADE

class GradeSerializer(serializers.Serializer):
    """
    Serializer for assigning grades (input).
    """
    student_id = serializers.IntegerField()
    semester_id = serializers.IntegerField()
    course_id = serializers.IntegerField()
    grade = serializers.FloatField()
    teacher_id = serializers.IntegerField(required=False, allow_null=True)

    def validate_grade(self, value):
        if not (MIN_GRADE <= value <= MAX_GRADE):
            raise serializers.ValidationError(
                f"Grade must be between {MIN_GRADE} and {MAX_GRADE}."
            )
        return value


class GradeResponseSerializer(serializers.Serializer):
    """
    Serializer for grade assignment response.
    """
    student = serializers.CharField()
    course = serializers.CharField()
    semester = serializers.CharField()
    grade = serializers.FloatField()
    teacher = serializers.CharField()