from rest_framework.serializers import ModelSerializer

from architects.models import Architect


class ArchitectSeializer(ModelSerializer):
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
        ]