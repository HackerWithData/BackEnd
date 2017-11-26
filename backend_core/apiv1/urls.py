from django.conf.urls import url
from .views.contractor_view import ContractorDetail

urlpatterns = [
    url(r'^contractors/(?P<object_id>[0-9]+)/$', ContractorDetail.as_view(), name='contractor_rest_api'),
]
