from django.conf.urls import url
from views import index

# TODO: rename home app to welcome app
urlpatterns = [
    url(r'^$', index, name='home_index'),
]