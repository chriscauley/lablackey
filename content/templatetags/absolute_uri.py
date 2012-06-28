from django import template

register = template.Library()


@register.filter
def absolute_uri(relative_url, request):
    return request.build_absolute_uri(relative_url)
