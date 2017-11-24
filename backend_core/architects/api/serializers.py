from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
)
from architects.models import Architect


class ArchitectSeializer(ModelSerializer):
    review = HyperlinkedIdentityField(view_name='review_api')
    overview = HyperlinkedIdentityField(view_name='overview_api')
    class Meta:
        model = Architect
        fields = [
            'review',
            'overview',
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
        ]