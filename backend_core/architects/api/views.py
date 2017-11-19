from .serializers import ArchitectSeializer
from architects.models import Architect

from rest_framework.generics import (
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
)

from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer

from django.shortcuts import HttpResponse


class ArchitectRetriveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Architect.objects.all()

    def get(self, request, *args, **kwargs):
        lic_num = self.request.resolver_match.kwargs[self.lookup_field]
        queryset = self.get_queryset().filter(lic_num=lic_num)
        info = ArchitectSeializer(queryset.first()).data
        content = JSONRenderer().render(info)
        return HttpResponse(content)


class ArchitectCreateAPIView(CreateAPIView):
    queryset = Architect.objects.all()
    serializer_class = ArchitectSeializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class ArchitectUpdateAPIView(UpdateAPIView):
    queryset = Architect.objects.all()
    serializer_class = ArchitectSeializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()
