from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from users.models import User
from users.permissions import IsAdminOrTeacher
from users.services import user_services

from academics.services.semester_services import get_semester_by_id
from academics.services.course_offering_services import get_teacher_courses_by_semester
from academics.serializers.course_offering_serializer import CourseOfferingSerializer

class TeacherCourseOfferingView(APIView):
    """
    API endpoint for retrieving courses assigned to a teacher by semester.
    - **Teachers** can view their own assigned courses.
    - **Admins** can view the assigned courses for any teacher (must include `teacher_id`).
    """

    permission_classes = [permissions.IsAuthenticated, IsAdminOrTeacher]

    @swagger_auto_schema(
        operation_summary="Retrieve a teacher's assigned courses by semester",
        operation_description=(
            "This endpoint allows **teachers** to view their assigned courses for a given semester, "
            "and **admins** to view the assigned courses for any teacher. \n\n"
            "**Rules:**\n"
            "- Teachers do not provide `teacher_id` (it’s taken from the authenticated user).\n"
            "- Admins must provide `teacher_id`.\n"
            "- The `semester_id` field is required."
        ),
        tags=["Courses"],
        manual_parameters=[
            openapi.Parameter(
                "semester_id",
                openapi.IN_QUERY,
                description="ID of the semester to filter courses",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
            openapi.Parameter(
                "teacher_id",
                openapi.IN_QUERY,
                description="ID of the teacher (required only for admins)",
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
        ],
        responses={
            200: "List of assigned courses",
            400: "Invalid request",
            403: "Permission denied",
            404: "Not found",
        },
    )
    def get(self, request):
        user = request.user
        semester_id: int = int(
            request.query_params.get("semester_id")
            )
        
        teacher_param = request.query_params.get("teacher_id")
        teacher_id: int = None
        if teacher_id is not None:
            teacher_id = int(teacher_param)
            
        if not semester_id:
            return Response(
                {"is_ok": False, "error": "semester_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            semester = get_semester_by_id(semester_id=semester_id)
        except ObjectDoesNotExist:
            return Response(
                {"is_ok": False, "error": "Invalid semester_id."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValidationError as e:
            return Response(
                {"is_ok": False, "error":  f"validation error {e}"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            teacher = user  
            if user.role == User.Role.ADMIN:
                if not teacher_id:
                    return Response(
                        {"is_ok": False, "error": "teacher_id is required for admins."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                teacher = user_services.get_user_by_id(user_id=teacher_id)
        except ObjectDoesNotExist:
            return Response(
                {"is_ok": False, "error": "Invalid teacher_id."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValidationError as e:
            return Response(
                Response({"is_ok": False, "error":  f"validation error {e}"}, status=status.HTTP_400_BAD_REQUEST)
            )
        
        try:
            offerings = get_teacher_courses_by_semester(teacher, semester)
            serializer = CourseOfferingSerializer(offerings, many=True)
            return Response(
                {"is_ok": True, "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            return Response({"is_ok": False, "error": f"validation error {e}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"is_ok": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        
        
