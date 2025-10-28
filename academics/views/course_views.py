from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from drf_yasg.utils import swagger_auto_schema

from django.core.exceptions import ValidationError
from users.permissions import IsAdmin

from academics.serializers.course_serializers import CourseSerializer
from academics.services.course_services import (
    create_course, 
    get_courses_by_ids,
    get_all_courses,
    )

class CourseView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        request_body=CourseSerializer,
        responses={201: "Created", 400: "Bad Request"},
        operation_summary="Registrar un nuevo curso",
        operation_description="permite crear nuevos cursos.",
        tags=["Courses"],
    )
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            prerrequisites = serializer.validated_data.get("prerequisites", [])
            prerrequisites_models = []
            if prerrequisites:
                prerrequisites_models = get_courses_by_ids(course_ids=prerrequisites)
            
            course = create_course(
                code=serializer.validated_data["code"],
                name=serializer.validated_data["name"],
                credits=serializer.validated_data["credits"],
                prerequisites=prerrequisites_models,
            )
        except ValidationError as e:
            return Response(
                {"is_ok": False, "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response_serializer = CourseSerializer(course)
        return Response(
            {"is_ok": True, "data": response_serializer.data},
            status=status.HTTP_201_CREATED,
        )
    
    @swagger_auto_schema(
        responses={200: CourseSerializer(many=True)},
        operation_summary="Listar cursos",
        operation_description="Devuelve la lista completa de cursos registrados.",
        tags=["Courses"],
    )
    def get(self, request):
        """Retrive all courses."""
        courses = get_all_courses()
        serializer = CourseSerializer(courses, many=True)
        return Response({"is_ok": True, "data": serializer.data}, status=status.HTTP_200_OK)