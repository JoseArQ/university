from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from users.permissions import IsAdmin  
from users.services import get_user_by_id

from academics.services.semester_services import get_semester_by_id
from academics.services.student_load_services import assign_semester_to_student
from academics.serializers.student_load_serializers import StudentLoadSemesterSerializer

class AssignSemesterToStudentView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        request_body=StudentLoadSemesterSerializer,
        responses={201: "Created", 400: "Bad Request"},
        operation_summary="Asignar semestre a estudiante",
        operation_description="Asigna un semestre a un estudiante y define su límite máximo de créditos.",
        tags=["Config"],
    )
    def post(self, request):
        serializer = StudentLoadSemesterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"is_ok": False, "errors": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            student = get_user_by_id(
                user_id=serializer.validated_data.get("student_id"),
                )
            semester = get_semester_by_id(
                semester_id=serializer.validated_data.get("semester_id"),
                )

            student_load = assign_semester_to_student(
                student=student, 
                semester=semester, 
                max_credits=serializer.validated_data.get("max_credits"),
                )
            
            response_data = StudentLoadSemesterSerializer(student_load).data

            return Response({"is_ok": True, "data": response_data},
                            status=status.HTTP_201_CREATED)

        except (ObjectDoesNotExist):
            return Response({"is_ok": False, "error": "Student or semester not found."},
                            status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"is_ok": False, "error": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"is_ok": False, "error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
