from django.conf.urls import url

from .views import (
    ProfessionalView,
    display_project_photos,
    upload_project_photos,
)
from review.views import submit_review, display_review
from photos.views import background_photo_upload

urlpatterns = [
    url(r'^([0-9]{0,8})/project-photos/$', display_project_photos, name='professional_project_photos'),
    url(r'^([0-9]{0,32})/$', ProfessionalView.as_view(), name='professional'),
    url(r'^([0-9]{0,8})/review/$', display_review, name='professional_review'),
    url(r'^([0-9]{0,8})/review/submit$', submit_review, name='professional_review_submit'),
    url(r'^([0-9]{0,8})/background-upload$', background_photo_upload, name='professional_background_photos_upload'),
    url(r'^([0-9]{0,8})/project-photos/upload$', upload_project_photos, name='professional_project_photos_upload'),

]
