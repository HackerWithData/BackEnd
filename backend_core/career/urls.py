from django.conf.urls import url
from views import display_career


urlpatterns = [
    url(r'^$', display_career, name='career'),
]