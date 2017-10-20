from django import template

from ..user_helpers import get_professional_and_professional_corresponding_object_by_user

register = template.Library()


@register.inclusion_tag('link/professional_homepage_link.html', takes_context=True)
def retrieve_professional_link(context):
    """
    assume the user is professional, should be bundled with is_professional
    retrieve corresponding professional object

    :param context:
    :return: rendered professional homepage link element
    """
    user = context['request'].user
    professional, professional_corresponding_object = get_professional_and_professional_corresponding_object_by_user(user)
    return {
        'professional': professional,
        'professional_corresponding_object': professional_corresponding_object
    }


@register.simple_tag(takes_context=True)
def is_professional(context):
    user = context['request'].user
    return user.role.upper() == 'PROFESSIONAL'

