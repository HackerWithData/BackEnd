from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from ..serializers.overview_serializer import OverviewSerializer
from overviews.models import Overview
from django.contrib.contenttypes.models import ContentType
from architects.models import Architect


class OverviewDetail(CreateAPIView):
    serializer_class = OverviewSerializer
    queryset = Overview.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        content_tpye = self.kwargs.pop('content_type', None)
        if content_tpye == 'architects':
            self.kwargs['content_type'] = ContentType.objects.get_for_model(model=Architect)
        serializer.save(**self.kwargs)
