from django.conf.urls import url
from views import upload_project_attachment, create_project, display_project

urlpatterns = [
    url(r'^$', display_project, name='display_project'),
    url(r'^attachment_upload/$', upload_project_attachment, name='upload_project_attachment_'),
    # TODO: need to write a more secure link
    url(r'^create/(.*?)/(.*?)$', create_project, name='create_project'),

    # url(r'^success/$', views.edit_success, name='edit_success'),
]
