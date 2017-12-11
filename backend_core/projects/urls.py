from django.conf.urls import url
from .views import upload_project_attachment, upload_project_photo, \
    create_project, display_project_overview, ProjectDetail, edit_project
from .helplers import validate_hoome_id
urlpatterns = [
    url(r'^$', display_project_overview, name='display_project_overview'),
    url(r'^(?P<uuid>[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})/$',
        ProjectDetail.as_view(), name='display_project_detail'),
    url(r'^attachment_upload/$', upload_project_attachment, name='upload_project_attachment'),
    url(r'^photo_upload/$', upload_project_photo, name='upload_project_photo'),
    # TODO: need to write a more secure link
    url(r'^create/$', create_project, name='create_project_direct'),
    url(r'^create/(.*?)/(.*?)/$', create_project, name='create_project'),
    url(r'^edit/(?P<uuid>[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})$', edit_project,
        name='edit_project'),

    url(r'^validation/$', validate_hoome_id, name='validate_hoome_id'),
    # url(r'^success/$', views.edit_success, name='edit_success'),
]
