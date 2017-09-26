from django.conf.urls import url
from views import display_privacy


urlpatterns = [
    url(r'privacy$', display_privacy, name='privacy'),
]