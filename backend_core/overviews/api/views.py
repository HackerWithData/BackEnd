from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from architects.models import Architect

from .serializers import OverviewSerializer
from ..models import Overview


class OverviewCreateAPIView(CreateAPIView):
    serializer_class = OverviewSerializer
    queryset = Overview.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            lic_num = self.request.resolver_match.kwargs['pk']
            architect = Architect.objects.get(lic_num=lic_num)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return super(OverviewCreateAPIView, self).create(request, *args, **kwargs)