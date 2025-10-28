from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema

from users.permissions import IsAdmin

from academics.serializers.teacher_load_serializers import TeacherLoadAssignSerializer
from academics.services.teacher_load_services import assign_semester_to_teacher
from academics.services.semester_services import get_semester_by_id

from users.services import get_user_by_id

class TeacherLoadAssignView(APIView):
    """
    API view to assign a semester to a teacher with a maximum credit limit.
    Only admins can perform this action.
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        request_body=TeacherLoadAssignSerializer,
        responses={201: "Created", 400: "Bad Request"},
        operation_summary="Asignar semestre a profesor",
        operation_description="Permite asignar un semestre a un profesor especificando su límite máximo de créditos.",
        tags=["Config"],
    )
    def post(self, request):
        serializer = TeacherLoadAssignSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"is_ok": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        validated_data = serializer.validated_data
        try:
            teacher = get_user_by_id(user_id=validated_data["teacher_id"])
            semester = get_semester_by_id(semester_id=validated_data["semester_id"])

            teacher_load = assign_semester_to_teacher(
                teacher=teacher,
                semester=semester,
                max_credits=validated_data["max_credits"],
            )
            return Response(
                {
                    "is_ok": True,
                    "data": {
                        "teacher": teacher_load.teacher.username,
                        "semester": str(teacher_load.semester),
                        "max_credits": teacher_load.max_credits,
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"is_ok": False, "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
