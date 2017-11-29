from rest_framework.serializers import ModelSerializer
from architects.models import Architect
from overviews.models import Overview
from review.models import Review


class OverviewSerializer(ModelSerializer):
    class Meta:
        model = Overview
        fields = ['overview']


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ['review']


class ArchitectSeializer(ModelSerializer):

    reviews = ReviewSerializer(many=True)
    overviews = OverviewSerializer(many=True)

    class Meta:
        model = Architect
        fields = [
            'lic_num',
            'lic_prefix',
            'lic_name',
            'lic_type',
            'lic_status',
            'lic_issue_date',
            'lic_expire_date',
            'street_address',
            'city',
            'county',
            'state',
            'country',
            'pos_code',
            'actions',
            'architect_uuid',
            'overviews',
            'reviews',
        ]
        read_only_fields = (
            'architect_uuid',
            'reviews',
            'overviews',
        )

