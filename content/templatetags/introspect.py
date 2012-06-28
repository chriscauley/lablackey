import cgi
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def introspect(obj):
    out = []
    out.append('<pre>')
    out.append(cgi.escape(repr(obj)))
    for key in dir(obj):
        out.append('  %s=%s' % (key, cgi.escape(str(getattr(obj, key)))))
    out.append('</pre>')
    return mark_safe('\n'.join(out))


@register.filter
def moduleclassname(obj):
    if getattr(obj, '__class__', None) is None:
        return 'not a class instance: %r' % (obj,)
    return '%s.%s' % (obj.__class__.__module__, obj.__class__.__name__)
