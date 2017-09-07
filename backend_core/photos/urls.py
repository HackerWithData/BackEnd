from django.conf.urls import url
from .views import FileFieldUpload, background_photo_upload


urlpatterns = [url(r'test1$', FileFieldUpload, name='test1_upload'),
               url(r'test2$', background_photo_upload, name='test2_upload'),
               ]