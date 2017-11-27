from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)
from architects.models import Architect
from django.contrib.contenttypes.models import ContentType
from overviews.models import Overview
from .overview_serializer import OverviewSerializer
from review.models import Review
from .review_serializer import ReviewSerializer
from django.contrib.contenttypes.models import ContentType


class AddOverview(HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        lookup_value = getattr(obj, self.lookup_field)
        kwargs = {self.lookup_url_kwarg: lookup_value}
        kwargs['object_id'] = kwargs.pop('pk')
        kwargs['content_type'] = 'architects'
        print "++++++++++"
        print kwargs
        return self.reverse(view_name, kwargs=kwargs, request=request, format=format)


class ArchitectSeializer(ModelSerializer):

    addoverview = AddOverview(view_name='apiv1:overview_rest_api')
    # addreview = HyperlinkedIdentityField(view_name='apiv1:review_rest_api', lookup_field='obj')
    reviews = SerializerMethodField()
    overviews = SerializerMethodField()

    class Meta:
        model = Architect
        fields = [
            # 'addreview',
            'addoverview',
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
            'overviews',
            'reviews'
        ]

    def get_overviews(self, obj):
        content_type = ContentType.objects.get_for_model(model=obj.__class__)
        qs = Overview.objects.all().filter(content_type=content_type, object_id=obj.lic_num)
        return OverviewSerializer(qs, many=True).data

    def get_reviews(self, obj):
        content_type = ContentType.objects.get_for_model(model=obj.__class__)
        qs = Review.objects.all().filter(content_type=content_type, object_id=obj.lic_num)
        return ReviewSerializer(qs, many=True).data
