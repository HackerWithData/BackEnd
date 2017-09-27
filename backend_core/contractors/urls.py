from django.conf.urls import url
from views import display_contractor,upload_project_photos, display_project_photos
from review.views import submit_review, display_review
from photos.views import background_photo_upload


urlpatterns = [
    url(r'^([0-9]{0,8})/review/$', display_review, name='contractor_review'),
    url(r'^([0-9]{0,8})/project-photos/$', display_project_photos, name='contractor_project_photos'),
    url(r'^([0-9]{0,8})/project-photos/upload$', upload_project_photos, name='contractor_project_photos_upload'),
    url(r'^([0-9]{0,8})/background-upload$', background_photo_upload, name='contractor_background_photos_upload'),
    url(r'^([0-9]{0,8})/review/submit$', submit_review, name='contractor_review_submit'),
    url(r'^([0-9]{0,8})/$', display_contractor, name='contractor'),
]