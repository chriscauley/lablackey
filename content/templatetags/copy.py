from django import template
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from sorl.thumbnail import get_thumbnail
from lablackey.content.models import Copy, DesignImage

register = template.Library()

@register.filter
def print_copy(context):
  c,new = Copy.objects.get_or_create(context=context)
  return mark_safe(c.body)
print_copy.is_safe=True

@register.simple_tag
def print_img(context,args=None):
  img, new = DesignImage.objects.get_or_create(context=context)
  opts = load_defaults({ 'crop': 'center','upscale': True,'quality': 95, },args)
  if not 'size' in opts:
    if True: #try:
      tn = img.src
    else: #except:
      tn = DesignImage.objects.get_or_create(context="default")[0].src
  else:
    tn = get_thumbnail(img.src,opts.pop('size'),**opts)
  attr = { 'src': tn.url,
       'width': tn.width,
       'height': tn.height,
       'alt': img.alt_text,  #eventually should default to alt_text OR caption OR...
       'class': context
       }
  s = """<img src="%(src)s" width="%(width)s" height="%(height)s" alt="%(alt)s" class="%(class)s"/>"""%attr
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

@register.filter
def photo_url (photo, size, opts={}):
  img = photo.src
  defaults = { 'crop': 'center','upscale': True,'quality': 95, 'size': '50x50' }
  opts.update(defaults)
  tn = get_thumbnail(img, size, **opts)
  return tn.url

@register.filter
def bw_override_thumbnail (photo, size):
  return override_thumbnail(photo, size, opts={'bw': True})

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
