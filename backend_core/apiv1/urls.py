from django.conf.urls import url
from .views.contractor_view import ContractorDetail
from .views.architect_view import ArchitectDetail
from .views.review_view import ReviewDetail
from .views.overview_view import OverviewDetail

urlpatterns = [
    url(r'^contractors/(?P<object_id>[0-9]+)/$', ContractorDetail.as_view(), name='contractor_rest_api'),
    url(r'^architects/(?P<object_id>[0-9]+)/$', ArchitectDetail.as_view(), name='architect_rest_api'),
    url(r'^(?P<content_type>architects)/(?P<object_id>[0-9]+)/review/$', ReviewDetail.as_view(), name='review_rest_api'),
    url(r'^(?P<content_type>architects)/(?P<object_id>[0-9]+)/overview/$', OverviewDetail.as_view(), name='overview_rest_api'),
]
