from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from rest_framework.response import Response
from rest_framework import status
from architects.models import Architect
from ..serializers.architect_serializer import ArchitectSeializer
from ..utils import (
    get_overviews,
    get_reviews,
)


class ArchitectDetail(APIView):

    get_permission_classes = [IsAuthenticated]
    post_permission_classes = [IsAdminUser]

    def get_permissions(self):
        safe_request_method = ("GET", "OPTIONS", "HEAD")
        unsafe_request_method = ("PUT", "POST")
        if self.request._request.method in safe_request_method:
            return [permission() for permission in self.get_permission_classes]
        if self.request._request.method in unsafe_request_method:
            return [permission() for permission in self.post_permission_classes]

    def get_object(self, architect_uuid):
        try:
            return Architect.objects.get(architect_uuid=architect_uuid)
        except Architect.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        architect_uuid = kwargs['architect_uuid']
        architect = self.get_object(architect_uuid)
        if architect is None:
            return Response(status=status.HTTP_204_NO_CONTENT)
        architect.reviews = get_reviews(architect)
        architect.overviews = get_overviews(architect)
        serializer = ArchitectSeializer(architect)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        architect = self.get_object(kwargs['architect_uuid'])
        serializer = ArchitectSeializer(architect, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ArchitectCreate(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ArchitectSeializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

