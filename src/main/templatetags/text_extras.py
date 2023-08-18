""" Template tags for the main app """

from django import template

register = template.Library()


# Tags
@register.assignment_tag
def query(qs, id):
    return qs.get(id=id)


@register.assignment_tag
def query2(qs, **kwargs):
    return qs.filter(**kwargs)
