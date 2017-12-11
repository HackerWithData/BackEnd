from django import template
from django.http import HttpResponse
from django.http.response import HttpResponseBadRequest
import json
from users.utils import ROLE_CHOICES, PROFESSIONAL, CONSUMER
from users.models import User
register = template.Library()


# In Test. Not Ready for use
# TODO: what's the point? find the name of object. It seems rare to use.
@register.filter
def get_object_name_for_this_content_type(obj):
    if not obj:
        return False
    return obj.content_type.get_object_for_this_type(pk=obj.object_id).name


def validate_hoome_id(request):
    if request.is_ajax() and request.method == "POST":
        data = json.loads(request.body)
        created_by = data.get('created_by', None)
        hoome_id = data.get('hoome_id', None)

        if not hoome_id:
            return HttpResponse(json.dumps({'status': 'error', 'error_message': 'Hoome id cannot be empty'}))
        else:
            try:
                user = User.objects.get(hoome_id=hoome_id)
            except:
                return HttpResponse(json.dumps({'status': 'error', 'error_message': "Hoome id does not exist"}))
        if user.role == PROFESSIONAL and created_by == PROFESSIONAL:
            return HttpResponse(json.dumps({'status': 'error', 'error_message': "Homeowener's hoome id does not exist"}))
        if user.role == CONSUMER and created_by == CONSUMER:
            return HttpResponse(json.dumps({'status': 'error', 'error_message': "Professional's hoome id does not exist"}))
        return HttpResponse(json.dumps({'status': 'success', 'error_message': ''}))
    else:
        return HttpResponseBadRequest
