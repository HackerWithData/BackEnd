from django.contrib.contenttypes.models import ContentType

from .models import (
    Rating,
    UserRating,
    RATING_STAR_MAX,
)


def avg_rating(review=None, rt=None):
    if not review or not rt:
        return None
    s = 0
    l = 0
    if review:
        for r in review:
            rate_list = [i.rating_score for i in r.userrating_set.all() if i.rating_type == rt]
            s += sum(rate_list)
            l += len(rate_list)
        try:
            return s * 1.0 / l
        except ZeroDivisionError:
            return 0
    else:
        return 0


def get_ratings(model_name=None, object_id=None, review=None):
    if not model_name or not object_id or not review:
        return None
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


def create_user_rating(user_rating_form, review):
    for field in user_rating_form.cleaned_data:
        UserRating.objects.create(
            review=review,
            rating_type=field[0].upper(),
            rating_score=int(user_rating_form.cleaned_data[field]),
        )
