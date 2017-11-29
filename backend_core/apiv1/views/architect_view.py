from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from architects.models import Architect
from ..serializers.architect_serializer import ArchitectSeializer
from ..utils import (
    get_overviews,
    get_reviews,
)


class ArchitectDetail(APIView):

    permission_classes = [IsAuthenticated]

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
        architect_uuid = kwargs['architect_uuid']
        architect = self.get_object(architect_uuid)
        serializer = ArchitectSeializer(architect, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)