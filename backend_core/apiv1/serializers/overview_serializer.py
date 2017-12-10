from overviews.models import Overview
from rest_framework.serializers import ModelSerializer


class OverviewSerializer(ModelSerializer):
    class Meta:
        model = Overview
        fields = [
            'overview',
            'object_id',
            'content_type',
        ]
        read_only_fields = [
            'object_id',
            'content_type',
        ]