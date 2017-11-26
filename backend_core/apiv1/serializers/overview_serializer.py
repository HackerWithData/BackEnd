from overviews.models import Overview
from rest_framework.serializers import ModelSerializer


class OverviewSerializer(ModelSerializer):
    class Meta:
        model = Overview
        fields = [
            'overview',
        ]