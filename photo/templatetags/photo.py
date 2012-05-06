from django import template
from django.conf import settings
from sorl.thumbnail import get_thumbnail

register = template.Library()

@register.filter
def nocrop_thumbnail (photo, size,opts={}):
  """A thumbnail tag that retains the original dimensions and shows the entire thumbnail"""
  size = size.split('x')
  rsize = (int(size[0]), int(size[1]))
  ratio = photo.width/float(photo.height)
  img = photo.src

  opts['crop'] = 'center'
  opts['upscale'] = True
  if rsize[0]/float(rsize[1])<ratio:
    rsize = (rsize[0],int(rsize[0]/ratio))
  else:
    rsize = (int(rsize[1]*ratio),rsize[1])
  return get_thumbnail(img,'%sx%s'%rsize, quality=95, **opts).url

@register.filter
def thumbnail (photo, size,opts={}):
  img = photo.src
  opts['crop'] = 'center'
  opts['upscale'] = True
  return get_thumbnail(img,size, quality=95, **opts).url
