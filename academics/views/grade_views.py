from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from users.models import User
from users.permissions import IsAdminOrTeacher
from users.services import user_services

from academics.serializers.grade_serializers import GradeSerializer, GradeResponseSerializer
from academics.services.grade_student_services import grade_student_in_course
from academics.services.semester_services import get_semester_by_id
from academics.services.course_services import get_course_by_id

class GradeView(APIView):
    """
    API endpoint for assigning grades to students.
    - **Admins** can assign grades on behalf of any teacher (must include `teacher_id`).
    - **Teachers** can only assign grades for their own courses (no `teacher_id` required).
    """

    permission_classes = [permissions.IsAuthenticated, IsAdminOrTeacher]

    @swagger_auto_schema(
        request_body=GradeSerializer,
        operation_summary="Assign a grade to a student",
        operation_description=(
            "This endpoint allows a **teacher** or **admin** to assign a grade to a student "
            "for a specific course and semester. \n\n"
            "**Rules:**\n"
            "- Teachers can only assign grades for courses they teach.\n"
            "- Admins can assign grades for any course and must specify a `teacher_id`.\n"
            "- Grade must be between the defined MIN_GRADE and MAX_GRADE constants (e.g., 0.0–5.0)."
        ),
        tags=["Grades"],
        responses={201: "Created", 400: "Bad Request", 500: "Internal server error"},
    )
    def post(self, request):
        """
        Handle POST request to assign a grade to a student.
        """
        user = request.user
        serializer = GradeSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            teacher = user
            if user.role == User.Role.ADMIN:
                teacher_id = serializer.validated_data.get("teacher_id")
                if not teacher_id:
                    return Response(
                        {"error": "teacher_id is required for admins."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                teacher = user_services.get_user_by_id(
                    user_id=teacher_id,
                )

            student = user_services.get_user_by_id(
                user_id=serializer.validated_data.get("student_id")
            )
           
            semester = get_semester_by_id(
                semester_id=serializer.validated_data.get("semester_id"),
            )

            course = get_course_by_id(
                course_id=serializer.validated_data.get("course_id"),
            )
                 
            enrollment = grade_student_in_course(
                teacher=teacher,
                student=student,
                semester=semester,
                course=course,
                grade=serializer.validated_data.get("grade"),
            )

            response_serializer = GradeResponseSerializer(enrollment)
            return Response(
                {"is_ok": True, "data": response_serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except (ObjectDoesNotExist):
            return Response(
                {"error": "Invalid student, semester, or course ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValidationError as e:
            return Response({"is_ok": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            return Response({"is_ok": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"is_ok": False, "error": f"Unexpected error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
