from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from academics.serializers.semester_serializers import SemesterSerializer
from academics.services.semester_services import create_semester, list_semesters

from users.permissions import IsAdmin


class SemesterView(APIView):
    """
    API View for creating and listing academic semesters.
    Only admin users are allowed to access this endpoint.
    """

    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        operation_summary="List all semesters",
        responses={200: SemesterSerializer(many=True)},
        tags=["Config"],
    )
    def get(self, request):
        """List all semesters in chronological order."""
        semesters = list_semesters()
        serializer = SemesterSerializer(semesters, many=True)
        return Response({"is_ok": True, "data": serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a new semester",
        request_body=SemesterSerializer,
        responses={201: SemesterSerializer, 400: "Validation error"},
         tags=["Config"],
    )
    def post(self, request):
        """Create a new academic semester."""
        serializer = SemesterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"is_ok": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            semester = create_semester(**serializer.validated_data)
        except Exception as e:
            return Response(
                {"is_ok": False, "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response_data = SemesterSerializer(semester).data
        return Response(
            {"is_ok": True, "data": response_data},
            status=status.HTTP_201_CREATED,
        )