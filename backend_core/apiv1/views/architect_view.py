from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from architects.models import Architect
from ..serializers.architect_serializer import ArchitectSeializer


class ArchitectDetail(RetrieveAPIView):
    queryset = Architect.objects.all()
    # use the function in apiv1.permission.py
    permission_classes = [IsAuthenticated]
    serializer_class = ArchitectSeializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_object(self):
        lic_num = self.kwargs['object_id']
        try:
            return Architect.objects.get(pk=lic_num)
        except Architect.DoesNotExist:
            return None
