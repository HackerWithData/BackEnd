from django.conf.urls import url
from views import ArchitectDetail, upload_project_photos, display_project_photos
from photos.views import background_photo_upload
from review.views import submit_review, display_review

urlpatterns = [
    url(r'^([0-9]{0,8})/$', ArchitectDetail.as_view(), name='architect'),
    url(r'^([0-9]{0,8})/project-photos/$', display_project_photos, name='architect_project_photos'),
    url(r'^([0-9]{0,8})/project-photos/upload$', upload_project_photos, name='architect_project_photos_upload'),
    url(r'^([0-9]{0,8})/background-upload$', background_photo_upload, name='architect_background_photos_upload'),
    url(r'^([0-9]{0,8})/review/$', display_review, name='architect_review'),
    url(r'^([0-9]{0,8})/review/submit$', submit_review, name='architect_review_submit'),
]
