from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from ..serializers.register_user_serializers import StudentRegisterSerializer, TeacherRegisterSerializer
from ..services import user_services
from ..permissions import IsAdmin


class StudentRegisterView(APIView):
    """
    API view for registering a new student user.
    Validates input data via serializer and creates user through the service layer.
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        request_body=StudentRegisterSerializer,  
        responses={201: "Created", 400: "Bad Request"},
        operation_summary="Registrar estudiante",
        operation_description="Crea un nuevo usuario con rol estudiante."
    )
    def post(self, request, *args, **kwargs):
        serializer = StudentRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = user_services.create_user_student(
                username=serializer.validated_data["username"],
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
                enrollment_number=serializer.validated_data["enrollment_number"],
                program=serializer.validated_data["program"],
            )
            return Response(
                {"is_ok": True, "data": {"id": user.id, "role": user.role}},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"is_ok": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class TeacherRegisterView(APIView):
    """
    API view for registering a new teacher user.
    Validates input data via serializer and creates user through the service layer.
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        request_body=TeacherRegisterSerializer,  
        responses={201: "Created", 400: "Bad Request"},
        operation_summary="Registrar estudiante",
        operation_description="Crea un nuevo usuario con rol profesor."
    )
    def post(self, request, *args, **kwargs):
        serializer = TeacherRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = user_services.create_user_teacher(
                username=serializer.validated_data["username"],
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
                department=serializer.validated_data["department"],
            )
            return Response(
                {"is_ok": True, "data": {"id": user.id, "role": user.role}},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"is_ok": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
