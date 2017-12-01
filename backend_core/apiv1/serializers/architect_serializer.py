from rest_framework.serializers import ModelSerializer
from architects.models import Architect
from overviews.models import Overview
from review.models import Review
from ..utils import get_uuid


class OverviewSerializer(ModelSerializer):
    class Meta:
        model = Overview
        fields = ['overview']


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ['review']


class ArchitectSeializer(ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    overviews = OverviewSerializer(many=True, read_only=True)

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
        )

    def create(self, validated_data):
        validated_data['architect_uuid'] = get_uuid(model=self.Meta.model, uuid_field_name='architect_uuid')
        return super(ArchitectSeializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data['lic_num'] = getattr(instance, 'lic_num')
        return super(ArchitectSeializer, self).update(instance, validated_data)
