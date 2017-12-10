"""backend_core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from views import (
    sign_up_complete_info,
    DashboardAfterPasswordChangeView,
    DashboardAfterPasswordSetView,
    ProfessionalProfileAfterSignupView,
    ConsumerProfileAfterSignupView,
    ConsumerProfileView,
    ProfessionalProfileView,
    Login,
    Signup
)

urlpatterns = [
    url(r'^signup/$', Signup.as_view(), name='account_signup'),
    url(r'^signup/info/$', sign_up_complete_info, name='account_signup_complete_info'),
    url(r'^signup/info/consumer/$', ConsumerProfileAfterSignupView.as_view(), name='account_consumer_profile_after_signup'),
    url(r'^signup/info/profession/$', ProfessionalProfileAfterSignupView.as_view(), name='account_professional_profile_after_signup'),
    url(r'^password/change/$', DashboardAfterPasswordChangeView.as_view(), name='account_change_password'),
    url(r'^password/set/$', DashboardAfterPasswordSetView.as_view(), name='account_set_password'),
    url(r'^consumer_profile/$', ConsumerProfileView.as_view(), name='account_consumer_profile'),
    url(r'^professional_profile/$', ProfessionalProfileView.as_view(), name='account_professional_profile'),
    url(r'^login/', Login.as_view(), name='account_login'),
]