from django.conf.urls import url
from views import display_architects

urlpatterns = [
    url(r'^(\w{1}[0-9]{0,8})/$', display_architects, name='architect'),
]
