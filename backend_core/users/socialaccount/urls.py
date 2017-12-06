from django.conf.urls import url
from allauth.socialaccount import views
from .views import Signup


urlpatterns = [
    url(r'^login/cancelled/$', views.login_cancelled,
        name='socialaccount_login_cancelled'),
    url(r'^login/error/$', views.login_error,
        name='socialaccount_login_error'),
    url(r'^signup/$', Signup.as_view(), name='socialaccount_signup'),
    url(r'^connections/$', views.connections, name='socialaccount_connections')
]
