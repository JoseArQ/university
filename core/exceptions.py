from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """
    Custom handler for authentication and permission errors.
    Returns standardized API responses.
    """
    response = exception_handler(exc, context)

    if response is not None:
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            return Response(
                {"is_ok": False, "error": "Authentication failed or token missing."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        elif response.status_code == status.HTTP_403_FORBIDDEN:
            return Response(
                {"is_ok": False, "error": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

    # fallback
    return response
