from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _


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
