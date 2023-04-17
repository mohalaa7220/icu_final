from rest_framework import status
from rest_framework.response import Response


def serializer_error(serializer):
    new_error = {}
    for field_name, field_errors in serializer.errors.items():
        new_error[field_name] = field_errors[0]
    return Response(new_error, status=status.HTTP_400_BAD_REQUEST)
