from django.conf.urls import url
from views import submit_review



urlpatterns=[url(r'^$', submit_review, name='review'),
                ]