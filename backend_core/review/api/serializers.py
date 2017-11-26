from rest_framework.serializers import ModelSerializer
from review.models import Review


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'project_type',
            'project_date',
            'project_address',
            'project_zipcode',
            'project_cost',
            'project_duration',
            'user',
            'comments',
            'is_anonymous',
            'review_status',
            'review_date',
            'content_type',
            'object_id',
        ]