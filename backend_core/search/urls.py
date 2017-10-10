from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^test/$', views.search_dispatch_test, name='search_dispatch_test'),
    url(r'^$', views.search_new, name='search_new'),
]
