from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from architects.models import Architect
from ..serializers.architect_serializer import ArchitectSeializer


class ArchitectDetail(RetrieveAPIView):
    queryset = Architect.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ArchitectSeializer

    def get_object(self):
        lic_num = self.kwargs['object_id']
        try:
            return Architect.objects.get(pk=lic_num)
        except Architect.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)