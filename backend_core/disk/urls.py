

from django.conf.urls import url
from django.contrib import admin
from views import uploads

urlpatterns = [url(r"^$", uploads),]