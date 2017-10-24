from django import template

register = template.Library()


# In Test. Not Ready for use
@register.filter
def get_object_name_for_this_content_type(obj):
    if not obj:
        return False
    return obj.content_type.get_object_for_this_type(pk=obj.object_id).name