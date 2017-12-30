from django.conf.urls import url
from views import MeisterDetail, upload_project_photos, display_project_photos
from review.views import submit_review, display_review
from photos.views import background_photo_upload

urlpatterns = [
    url(r'^([0-9]{0,64})/review/$', display_review, name='meister_review'),
    url(r'^([0-9]{0,64})/project-photos/$', display_project_photos, name='meister_project_photos'),
    url(r'^([0-9]{0,64})/project-photos/upload$', upload_project_photos, name='meister_project_photos_upload'),
    url(r'^([0-9]{0,64})/background-upload$', background_photo_upload, name='meister_background_photos_upload'),
    url(r'^([0-9]{0,64})/review/submit$', submit_review, name='meister_review_submit'),
    url(r'^([0-9]{0,64})/$', MeisterDetail.as_view(), name='meister'),
]
