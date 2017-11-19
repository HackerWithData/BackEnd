from django.conf.urls import url
from .views import (
    ArchitectRetriveAPIView,
    ArchitectCreateAPIView,
    ArchitectUpdateAPIView,
)


urlpatterns = [
    url(r'^api/(?P<pk>[0-9]{0,8})/$', ArchitectRetriveAPIView.as_view(), name='architect_api_retrieve'),
    url(r'^api/create/$', ArchitectCreateAPIView.as_view(), name='architect_api_create'),
    url(r'^api/update/(?P<pk>[0-9]{0,8})/$', ArchitectUpdateAPIView.as_view(), name='architect_api_update'),
]