from django.conf.urls import url
from views import upload_project_attachment, create_project, display_project_overview, display_project_detail

urlpatterns = [
    url(r'^$', display_project_overview, name='display_project_overview'),
    url(r'^(\d+)/$', display_project_detail, name='display_project_detail'),
    url(r'^attachment_upload/$', upload_project_attachment, name='upload_project_attachment'),
    # TODO: need to write a more secure link
    url(r'^create/(.*?)/(.*?)$', create_project, name='create_project'),

    # url(r'^success/$', views.edit_success, name='edit_success'),
]
