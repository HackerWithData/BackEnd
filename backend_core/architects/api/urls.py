from .views import ArchitectRetrieveAPIView
from review.api.views import ReviewCreateAPIView
from overviews.api.views import OverviewCreateAPIView

from django.conf.urls import url
urlpatterns = [
    url(r'api/(?P<pk>[0-9]{0,8})/$', ArchitectRetrieveAPIView.as_view(), name='architect_api'),
    url(r'api/(?P<pk>[0-9]{0,8})/review', ReviewCreateAPIView.as_view(), name='review_api'),
    url(r'api/(?P<pk>[0-9]{0,8})/overview', OverviewCreateAPIView.as_view(), name='overview_api'),
]