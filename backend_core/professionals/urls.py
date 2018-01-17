from django.conf.urls import url

from .views import (
    ProfessionalView,
    display_project_photos,
    upload_project_photos,
    submit_review,
    display_review,
    background_photo_upload,
)

uuid = r'^([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})'

urlpatterns = [
    url(r'^([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})/project-photos/$',
        display_project_photos, name='professional_project_photos'),
    url(r'^([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})/$',
        ProfessionalView.as_view(), name='professional'),
    url(r'^([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})/review/$',
        display_review, name='professional_review'),
    url(r'^([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})/review/submit$',
        submit_review, name='professional_review_submit'),
    url(r'^([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})/background-upload$',
        background_photo_upload, name='professional_background_photos_upload'),
    url(r'^([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})/project-photos/upload$',
        upload_project_photos, name='professional_project_photos_upload'),
]
