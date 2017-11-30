from review.models import Review
from overviews.models import Overview
from django.contrib.contenttypes.models import ContentType
from uuid import uuid4


def get_overviews(obj):
    content_type = ContentType.objects.get_for_model(model=obj.__class__)
    qs = Overview.objects.all().filter(content_type=content_type, object_id=obj.lic_num)
    return qs


def get_reviews(obj):
    content_type = ContentType.objects.get_for_model(model=obj.__class__)
    qs = Review.objects.all().filter(content_type=content_type, object_id=obj.lic_num)
    return qs


def get_uuid(model, uuid_field_name):
    flag = True
    while flag:
        try:
            uuid = uuid4()
            kwargs = {uuid_field_name: uuid}
            model.objects.get(**kwargs)
        except model.DoesNotExist:
            flag = False
    return uuid
