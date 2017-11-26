from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class ReviewSerializer(serializers.Serializer):
    comments = serializers.CharField(label=_('Comments'))
    # first_name = serializers.CharField(label=_('First Name'), max_length=25)
    # last_name = serializers.CharField(label=_('Last Name'), max_length=25)
    project_date = serializers.DateField(label=_('Project Date'))
    project_type = serializers.CharField(label=_('Project Type'), max_length=255)
    project_zipcode = serializers.CharField(label=_('Project Zipcode'), max_length=20)
    project_cost = serializers.IntegerField(label=_('Project Cost'))
    project_duration = serializers.IntegerField(label=_('Project Duration'))
    # email = serializers.CharField(label=_('Email'), max_length=254)
    project_address = serializers.CharField(label=_('Project Address'), max_length=100)
    is_anonymous = serializers.BooleanField(label=_('Is Anonymous?'), required=False)


class BondHistorySerializer(serializers.Serializer):
    surety_company = serializers.CharField(max_length=255)
    bond_num = serializers.CharField(max_length=20)
    bond_amount = serializers.CharField(max_length=20)
    bond_effective_date = serializers.DateField(read_only=True)
    bond_cancellation_date = serializers.DateField(read_only=True)


class WorkerCompensationHistorySerializer(serializers.Serializer):
    insur_company = serializers.CharField(max_length=255)
    policy_num = serializers.CharField(max_length=20)
    insur_effective_date = serializers.DateField(read_only=True)
    insur_cancellation_date = serializers.DateField(read_only=True)


class ComplaintOverallSerializer(serializers.Serializer):
    case = serializers.IntegerField(read_only=True)
    citation = serializers.IntegerField(read_only=True)
    arbitration = serializers.IntegerField(read_only=True)
    complaint = serializers.IntegerField(read_only=True)


class ContractorSerializer(serializers.Serializer):
    review = ReviewSerializer(many=True)
    bond_history = BondHistorySerializer()
    worker_compensation_history = WorkerCompensationHistorySerializer()
    complaint = ComplaintOverallSerializer()

    lic_num = serializers.IntegerField(read_only=True)
    lic_type = serializers.CharField(read_only=True)
    lic_name = serializers.CharField(max_length=255, read_only=True)
    lic_status = serializers.CharField(max_length=30, read_only=True)
    lic_issue_date = serializers.DateField(read_only=True)
    lic_expire_date = serializers.DateField(read_only=True)
    entity = serializers.CharField(max_length=25)
    street_address = serializers.CharField(max_length=255)
    csp = serializers.CharField(max_length=63, )
    state = serializers.CharField(max_length=63)
    pos_code = serializers.CharField(max_length=25)
    phone = serializers.CharField(max_length=25, )
    lic_status_add = serializers.CharField(read_only=True)
    bus_info_add = serializers.CharField(read_only=True)
    dba = serializers.CharField(max_length=255, read_only=True)
    length = serializers.IntegerField(read_only=True)
