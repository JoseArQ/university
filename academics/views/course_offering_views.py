from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from academics.services.course_services import get_course_by_id
from users.permissions import IsAdmin
from users.services.user_services import get_user_by_id

from academics.serializers.course_offering_serializer import CourseOfferingCreateSerializer
from academics.services.course_offering_services import create_course_offering
from academics.services.semester_services import get_semester_by_id

class CourseOfferingCreateView(APIView):
    """
    API View for creating a new CourseOffering.
    Only accessible to admin users.
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        request_body=CourseOfferingCreateSerializer,
        responses={201: "Created", 400: "Bad Request"},
        operation_summary="Crear oferta de curso",
        operation_description="Crea una nueva oferta de curso para un profesor en un semestre específico.",
        tags=["Courses"],
    )
    def post(self, request, *args, **kwargs):
        serializer = CourseOfferingCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"is_ok": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            teacher = get_user_by_id(
                user_id=serializer.validated_data.get("teacher_id")
            )
            semester_obj = get_semester_by_id(
                semester_id=serializer.validated_data.get("semester_id"),
                )
            course_obj = get_course_by_id(
                course_id=serializer.validated_data.get("course_id"),
            )
            offering = create_course_offering(
                teacher=teacher,
                semester=semester_obj,
                course=course_obj,
            )
            return Response(
                {
                    "is_ok": True,
                    "data": CourseOfferingCreateSerializer(offering).data,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"is_ok": False, "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
