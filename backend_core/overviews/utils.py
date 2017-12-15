from .models import Overview
from .forms import OverviewForm
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _,  ugettext_lazy as _


def get_overview(model_name, object_id, message):
    try:
        overview = Overview.objects.get(
            content_type=ContentType.objects.get(model=model_name),
            object_id=object_id,
        ).overview
    except Overview.DoesNotExist:
        overview = _(message)
    return overview


def get_overview_form(overview):
    overview_form = OverviewForm(initial={'overview': overview})
    return overview_form
