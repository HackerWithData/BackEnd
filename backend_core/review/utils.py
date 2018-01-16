from django.contrib.contenttypes.models import ContentType

from professionals.utils import check_professional_type
from ratings.models import UserRating, Rating
from photos.models import Photo
from .models import Review


def get_reviews(model_name=None, object_id=None, review_status=None):
    if not model_name or not object_id or not review_status:
        return None
    try:
        review = Review.objects.filter(
            content_type=ContentType.objects.get(model=model_name),
            object_id=object_id,
            review_status=review_status,
        )
    except ContentType.DoesNotExist:
        review = None
    return review


def create_review(request, o_id, review_form):
    model_type = check_professional_type(request)
    review = review_form.save(commit=False)
    if request.user.is_authenticated():
        review.user = request.user
    try:
        review.content_type = ContentType.objects.get(model=model_type)
    except ContentType.DoesNotExist:
        pass
    review.object_id = o_id
    review.save()
    return review


def create_review_photos(request, review):
    content_type = ContentType.objects.get(model='review')
    object_id = int(review.id)
    files = request.FILES.getlist('project photos')
    for f in files:
        Photo.objects.create(
            img=f,
            title=f.name,
            content_type=content_type,
            object_id=object_id,
        )


def update_accept_review(request):
    try:
        review = Review.objects.get(contractor=request.contractor)
        review.review_status = 'A'
        review.save()
    except Review.DoesNotExist:
        pass
    try:
        ur = UserRating.objects.get(review=review)
        for r in ur:
            try:
                rating = Rating.objects.get(contractor=request.contractor, rating_type=review.rating_type)
                rating.total = rating.total + r.rating_score
                rating.count = rating.count + 1
                if rating.count != 0:
                    rating.average = round(rating.total * 1.0 / rating.count, 2)
                else:
                    rating.average = 0
            except Rating.DoesNotExist:
                pass
    except UserRating.DoesNotExist:
        pass
