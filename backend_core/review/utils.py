from .models import Review
from .forms import ReviewForm
from django.contrib.contenttypes.models import ContentType
import datetime
from django.utils.translation import ugettext as _,  ugettext_lazy as _
from django.shortcuts import render, redirect
from professionals.utils import check_professional_type

from ratings.forms import UserRatingForm
from ratings.models import UserRating
from ratings.utils import create_user_rating
from photos.models import Photo
from django.contrib import messages
from photos.utils import upload_photo

def get_review(model_name, object_id, review_status):
    try:
        review = Review.objects.filter(
            content_type=ContentType.objects.get(model=model_name),
            object_id=object_id,
            review_status=review_status,
        )
    except:
        review = None
    return review


def get_review_form(request):
    if request.user.is_authenticated:
        review_form = ReviewForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'project_date': datetime.datetime.today().strftime('%Y-%m-%d'),
        })
    else:
        review_form = ReviewForm(initial={'project_date': datetime.datetime.today().strftime('%Y-%m-%d')})
    return review_form



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
    if len(files) > 0:
        for f in files:
            instance = Photo.objects.create(
                img=f,
                title=f.name,
                content_type=content_type,
                object_id=object_id,
            )
            instance.save()


def post_review(request, o_id, info_dict, template_name):
    user_rating_form = UserRatingForm(request.POST)
    review_form = ReviewForm(request.POST)
    if review_form.is_valid() and user_rating_form.is_valid():
        review = create_review(
            request=request,
            o_id=o_id,
            review_form=review_form,
        )
        create_user_rating(user_rating_form=user_rating_form, review=review)
        upload_photo(request=request, model_name='review', o_id=review.id)
        return redirect(request.path)
    else:
        info_dict['review_form'] = review_form
        info_dict["user_rating_form"] = user_rating_form
        messages.warning(request, _('Submit Failed. Please verify your content is correct.'))
        return render(request, template_name, {"info_dict": info_dict})


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
    return render(request, '/')