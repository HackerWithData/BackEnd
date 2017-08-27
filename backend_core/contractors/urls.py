from django.conf.urls import url, include
from views import display_contractor

urlpatterns = [
    url(r'(?P<slug>[-_\w]+)/$', display_contractor, name='contractor'),
]