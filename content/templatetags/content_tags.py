from django import template
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from sorl.thumbnail import get_thumbnail
from mwm.content.models import Copy, DesignImage
try:
  from settings.content_defaults import copy_defaults
except ImportError:
  copy_defaults = {}


register = template.Library()

@register.filter
def print_copy(context, default_text=None):
  defaults = {}
  if default_text:
    defaults['text'] = default_text
  elif context in copy_defaults:
    defaults['text'] = copy_defaults[context]
  c,new = Copy.objects.get_or_create(context=context, defaults=defaults)
  return mark_safe(c.text)
print_copy.is_safe=True

@register.simple_tag
def print_img(context,size=None,crop='center',upscale=True,quality=95,url=False):
  img, new = DesignImage.objects.get_or_create(context=context)
  width, height = size.split('x')
  if not img.src:
    if url:
      return ''
    return '<img width="%s" height="%s">' % (width, height)
  if not size:
    tn = img.src
  else:
    tn = get_thumbnail(img.src,size,crop=crop,upscale=upscale,quality=quality)
    width = tn.width
    height = tn.height
  attr = {
    's': tn.url,
    'w': width,
    'h': height,
    #'a': img.alt_text,  #eventually should default to alt_text OR caption OR...
    'c': context
    }
  if url:
    return tn.url
  s = '<img src="%(s)s" width="%(w)s" height="%(h)s" alt="" class="%(c)s"/>'%attr
  return s

@register.simple_tag
def print_img_url(context,args=None):
  img, new = DesignImage.objects.get_or_create(context=context)
  opts = load_defaults({ 'crop': 'center','upscale': True,'quality': 95, },args)
  if not 'size' in opts:
    tn = img.src
  else:
    tn = get_thumbnail(img.src,opts.pop('size'),**opts)
  return tn.url

def load_defaults(values,args):
  """
  Loads a string of "k1=v1,k2=v2..." into a dictionary of default values.
  Basically just compensates for simple_tags lack of *args and **kwargs.
  Probably not the best way to handle this.
  Holds the world record for most inappropriately long doc-string,
  if only by one line.
  """
  if args:
    values.update(dict([a.split("=") for a in args.split(",")]))
  return values
