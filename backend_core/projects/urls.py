from django.conf.urls import url
from views import upload_project_attachment, upload_project_photo, \
    create_project, display_project_overview, ProjectDetail


urlpatterns = [
    url(r'^$', display_project_overview, name='display_project_overview'),
    url(r'^(?P<uuid>[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})/$',
        ProjectDetail.as_view(), name='display_project_detail'),
    url(r'^attachment_upload/$', upload_project_attachment, name='upload_project_attachment'),
    url(r'^photo_upload/$', upload_project_photo, name='upload_project_photo'),
    # TODO: need to write a more secure link
    url(r'^create/(.*?)/(.*?)/$', create_project, name='create_project'),
    # url(r'^success/$', views.edit_success, name='edit_success'),
]
