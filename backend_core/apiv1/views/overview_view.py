from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from ..serializers.overview_serializer import OverviewSerializer
from overviews.models import Overview


class OverviewDetail(CreateAPIView):
    serializer_class = OverviewSerializer
    queryset = Overview.objects.all()
    permission_classes = [IsAuthenticated]