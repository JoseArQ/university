from rest_framework import serializers

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