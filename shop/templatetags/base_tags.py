from django import template
from ..models import Category
from django.template import RequestContext
register = template.Library()


@register.inclusion_tag("inc/category_navbar.html", takes_context=True)
def category_navbar(context):
    request = context['request']
    return {
        "categories": Category.objects.filter(status=True),
        'request': request
    }
