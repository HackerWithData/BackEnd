from django.conf.urls import url,include
from views import display_contractor
from review.views import submit_review, display_review

urlpatterns = [
    url(r'^([0-9]{0,8})/review/$', display_review, name='contractor_review'),
    url(r'^([0-9]{0,8})/review/submit$', submit_review, name='contractor_review_submit'),
    url(r'^([0-9]{0,8})/overview/$', display_contractor, name='contractor'),
]