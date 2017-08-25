from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^test/$', search_dispatch_test, name='search_dispatch_test'),
    url(r'^(?P<query_target>[-\w]+)/(?P<query_keywords>[-\w ]+)$/(?P<query_location>[-\w ]+)/$', search_new, name='search_new'),
]
