from django.conf.urls import url
from views import upload_project_attachment, upload_project

urlpatterns = [
    url(r'^attachment_upload/$', upload_project_attachment, name='project_attachment_upload'),
    #TODO: need to write a more secure link
    url(r'^upload/(.*?)/(.*?)$', upload_project, name='project_upload'),
    # url(r'^success/$', views.edit_success, name='edit_success'),
]