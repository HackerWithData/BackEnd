from django.conf.urls import url
from views import SubmitReview



urlpatterns=[url(r'^$', SubmitReview.as_view(), name='review'),
                ]