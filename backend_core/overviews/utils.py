from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _,  ugettext_lazy as _

from .models import Overview


def get_overview(model_name, object_id, message):
    try:
        overview = Overview.objects.get(
            content_type=ContentType.objects.get(model=model_name),
            object_id=object_id,
        ).overview
    except Overview.DoesNotExist:
        overview = _(message)
    return overview


def get_or_create_overview(content, model_name, o_id):
    overview, status = Overview.objects.get_or_create(
        content_type=ContentType.objects.get(model=model_name),
        object_id=o_id,
    )
    overview.overview = content
    overview.save()
