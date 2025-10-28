from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema

from users.models import User
from users.permissions import IsAdminOrStudent
from users.services.user_services import get_user_by_id

from academics.serializers.student_enrollment_serializers import StudentEnrollmentCreateSerializer
from academics.services.student_enrollment_services import enroll_student_in_course
from academics.services.semester_services import get_semester_by_id
from academics.services.course_services import get_course_by_id


class StudentEnrollmentView(APIView):
    """
    API view for students to enroll in a course for a given semester.
    Uses the service layer to handle business logic.
    """
    permission_classes = [permissions.IsAuthenticated, IsAdminOrStudent]

    @swagger_auto_schema(
        request_body=StudentEnrollmentCreateSerializer,
        responses={201: "Created", 400: "Bad Request"},
        operation_summary="Inscribir un estudiante a un curso",
        operation_description=(
            "Permite que un estudiante se inscriba a un curso, o que un admin inscriba a un estudiante."
        ),
        tags=["Enrollments"],
    )
    def post(self, request):
        serializer = StudentEnrollmentCreateSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            
            student = request.user
            if request.user.role == User.Role.ADMIN:
                student_id = serializer.validated_data.get("student_id")
                if not student_id:
                    return Response(
                        {"is_ok": False, "error": "student_id es requerido para administradores."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                student = get_user_by_id(student_id)

            semester = get_semester_by_id(serializer.validated_data.get("semester_id"))
            course = get_course_by_id(serializer.validated_data.get("course_id"))

            if request.user.role != User.Role.ADMIN and student != request.user:
                return Response(
                    {"is_ok": False, "error": "No puedes inscribir a otros estudiantes."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            enrollment = enroll_student_in_course(
                student=student,
                semester=semester,
                course=course,
            )

            return Response(
                {"is_ok": True, "data": serializer.to_representation(enrollment)},
                status=status.HTTP_201_CREATED,
            )

        except (ValidationError, ObjectDoesNotExist) as e:
            return Response(
                {"is_ok": False, "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {"is_ok": False, "error": f"Unexpected error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )