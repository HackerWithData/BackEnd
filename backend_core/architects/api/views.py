from .serializers import ArchitectSeializer
from architects.models import Architect

from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated


class ArchitectRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ArchitectSeializer
    queryset = Architect.objects.all()
