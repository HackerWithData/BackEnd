import datetime


from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _,  ugettext_lazy as _
from django.shortcuts import render, redirect
from django.contrib import messages

from professionals.utils import check_professional_type
from ratings.forms import UserRatingForm
from ratings.models import UserRating
from ratings.utils import create_user_rating
from photos.models import Photo
from photos.utils import upload_photo
from .models import Review
from .forms import ReviewForm


def get_reviews(model_name, object_id, review_status):
    try:
        review = Review.objects.filter(
            content_type=ContentType.objects.get(model=model_name),
            object_id=object_id,
            review_status=review_status,
        )
    except:
        review = None
    return review


def create_review(request, o_id, review_form):
    model_type = check_professional_type(request)
    review = review_form.save(commit=False)
    if request.user.is_authenticated():
        review.user = request.user
    review.content_type = ContentType.objects.get(model=model_type)
    review.object_id = o_id
    review.save()
    return review


def create_review_photos(request, review):
    content_type = ContentType.objects.get(model='review')
    object_id = int(review.id)
    files = request.FILES.getlist('project photos')
    for f in files:
        instance = Photo.objects.create(
            img=f,
            title=f.name,
            content_type=content_type,
            object_id=object_id,
        )
        instance.save()


def update_accept_review(request):
    review = Review.objects.get(contractor=request.contractor)
    review.review_status = 'A'
    review.save()
    ur = UserRating.objects.get(review=review)
    for r in ur:
        rating = Rating.objects.get(contractor=request.contractor, rating_type=review.rating_type)
        rating.total = rating.total + r.rating_score
        rating.count = rating.count + 1
        rating.average = round(rating.total * 1.0 / rating.count, 2)