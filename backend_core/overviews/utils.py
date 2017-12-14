from .models import Overview
from .forms import OverviewForm
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _,  ugettext_lazy as _


def get_overview(model_name, object_id, **kwargs):
    try:
        overview = Overview.objects.get(
            content_type=ContentType.objects.get(model=model_name),
            object_id=object_id,
        ).overview
    except Overview.DoesNotExist:
        overview = _("""{bus_name} is an architect from {city}. The company holds a license number according to {data_source}. 
            The License is verified as active when we checked last time. If you would like to know {bus_name} more, 
            please contact us and we will share more information about this architect to you.
            """).format(**kwargs)
    return overview


def get_overview_form(overview):
    overview_form = OverviewForm(initial={'overview': overview})
    return overview_form
