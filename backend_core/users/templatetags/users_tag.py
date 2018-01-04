import re
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


@register.simple_tag(takes_context=True)
def is_sign_up_completed(context):
    user = context['request'].user
    professional_profile = user.professional_profiles.first()
    if not professional_profile:
        return False
    professional = professional_profile.professional
    if not professional:
        return False
    return True


@register.simple_tag(takes_context=True)
def is_project_detail_link(context):
    # print(context['request'].GET)
    try:
        #multivalue key error
        redirect_url = context['request'].GET['next']
        project_num_pattern = "[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}"
        #print(1)
        if redirect_url is not None:
            el = redirect_url.split('/')
            # TODO: check project.uuid in database? set limit?
            if len(el) == 4 and el[1] == "project" and re.match(project_num_pattern, el[2]):
                #print(2)
                return True
            else:
                #print(3)
                return False
        else:
            #print(4)
            return False
    except:
        #print(5)
        return False