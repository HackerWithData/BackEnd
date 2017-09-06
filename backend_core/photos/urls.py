from django.conf.urls import url
from .views import FileFieldUpload


urlpatterns = [url(r'test$', FileFieldUpload, name='test_upload'),
               ]