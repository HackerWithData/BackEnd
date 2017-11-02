from django.conf.urls import url
from views import submit_review, display_review


urlpatterns = [url(r'^$', display_review, name='review'),
               # url(r'^/submit$', submit_review, name='review_submit'),
               ]
