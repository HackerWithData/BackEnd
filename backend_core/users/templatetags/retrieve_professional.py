from django import template

register = template.Library()


@register.filter(name='demotag')
def demotag(value):
    print value
    return value
