from .models import Rating, UserRating
from django.contrib.contenttypes.models import ContentType
from .forms import UserRatingForm

RATING_STAR_MAX = 10


def avg_rating(review, rt):
    s = 0
    l = 0
    if review:
        for r in review:
            rate_list = [i.rating_score for i in r.userrating_set.all() if i.rating_type == rt]
            s += sum(rate_list)
            l += len(rate_list)
        return s * 1.0 / l
    else:
        return 0


def get_ratings(model_name, object_id, review):
    rating = Rating.objects.filter(
        content_type=ContentType.objects.get(model=model_name),
        object_id=object_id,
    ).order_by('ratings_average')
    ratings = dict()
    ratings['stars'] = range(RATING_STAR_MAX, 0, -1)
    ratings['overall'] = (avg_rating(review, 'Q') + avg_rating(review, 'E') + avg_rating(review, 'L')) / 3
    try:
        ratings['rate'] = [(item.average, round(item.average * 1.0 / RATING_STAR_MAX, 2)) for item in
                           rating]
    except:
        pass
    return ratings


def get_user_rating_form():
    return UserRatingForm()


def create_user_rating(user_rating_form, review):
    for field in user_rating_form.cleaned_data:
        user_rating = UserRating(
            review=review,
            rating_type=field[0].upper(),
            rating_score=int(user_rating_form.cleaned_data[field]),
        )
        user_rating.save()
