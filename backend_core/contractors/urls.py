from django.conf.urls import url, include
from views import display_contractor
from review.views import submit_review
urlpatterns = [
    url(r'([0-9]{0,8})/overview/$', display_contractor, name='contractor'),
    url(r'([0-9]{0,8})/review/$', submit_review, name='contractor_review'),
]