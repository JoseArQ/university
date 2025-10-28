from rest_framework import serializers
from academics.models import Course

class CourseSerializer(serializers.ModelSerializer):
    prerequisites = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True
    )
    prerequisites_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = [
            "id", 
            "code", 
            "name", 
            "credits", 
            "prerequisites",
            "prerequisites_detail",
            ]
     
    def get_prerequisites_detail(self, obj):
        """Return readable prerequisite info."""
        return [
            {"id": c.id, "code": c.code, "name": c.name}
            for c in obj.prerequisites.all()
        ]