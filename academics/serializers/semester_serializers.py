from rest_framework import serializers
from academics.models import Semester


class SemesterSerializer(serializers.ModelSerializer):
    """
    Serializer for listing and creating semesters.
    """

    class Meta:
        model = Semester
        fields = ["id", "year", "term"]
        read_only_fields = ["id"]
