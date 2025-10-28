from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema

from users.serializers.profile_serializers import (
    StudentProfileSerializer,
    TeacherProfileSerializer,
)
from users.services import list_students, list_teachers
from ..permissions import IsAdmin


class StudentListView(APIView):
    """
    API view to list all students. Only accessible by admin users.
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        responses={200: StudentProfileSerializer(many=True)},
        operation_summary="Listar estudiantes",
        operation_description="Devuelve una lista de todos los estudiantes registrados en el sistema."
    )
    def get(self, request):
        students = list_students()
        serializer = StudentProfileSerializer(students, many=True)
        return Response(
            {"is_ok": True, "data": serializer.data},
            status=status.HTTP_200_OK
        )


class TeacherListView(APIView):
    """
    API view to list all teachers. Only accessible by admin users.
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        responses={200: TeacherProfileSerializer(many=True)},
        operation_summary="Listar profesores",
        operation_description="Devuelve una lista de todos los profesores registrados en el sistema."
    )
    def get(self, request):
        teachers = list_teachers()
        serializer = TeacherProfileSerializer(teachers, many=True)
        return Response(
            {"is_ok": True, "data": serializer.data},
            status=status.HTTP_200_OK
        )
