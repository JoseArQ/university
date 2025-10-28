from rest_framework import serializers

class TeacherLoadAssignSerializer(serializers.Serializer):
    teacher_id = serializers.IntegerField()
    semester_id = serializers.IntegerField()
    max_credits = serializers.IntegerField(min_value=1)
