from rest_framework import serializers
from academics.models import CourseOffering
class CourseOfferingCreateSerializer(serializers.Serializer):
    teacher_id = serializers.IntegerField()
    semester_id = serializers.IntegerField()
    course_id = serializers.IntegerField()
    
    def to_representation(self, instance):
        """
        Representación personalizada de la oferta de curso creada.
        """
        return {
            "id": instance.id,
            "teacher": instance.teacher.username,
            "semester": str(instance.semester),
            "course": instance.course.name,
        }

class CourseOfferingSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source="course.name", read_only=True)
    course_code = serializers.CharField(source="course.code", read_only=True)
    semester_name = serializers.CharField(source="semester.name", read_only=True)

    class Meta:
        model = CourseOffering
        fields = [
            "id",
            "course",
            "course_code",
            "course_name",
            "semester",
            "semester_name",
        ]