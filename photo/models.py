from django.db import models
from sorl.thumbnail import ImageField, get_thumbnail
from lablackey.db.models import OrderedModel
from crop_override import CropOverride, OriginalImage

class Photo(models.Model):
  name = models.CharField(max_length=512)
  src = OriginalImage(upload_to='uploads/photos/%Y-%m',max_length=300)
  square_crop = CropOverride('Square (1x1)', upload_to='some/dir', original='src', aspect='1x1')
  landscape_crop = CropOverride('Landscape (4x3)', upload_to='some/dir', original='src', aspect='4x3')
  portrait_crop = CropOverride('Portrait (3x4)', upload_to='some/dir', original='src', aspect='3x4')

  thumbnail = lambda self:'<img src="%s"/>'%(get_thumbnail(self.src, '128x128').url)
  thumbnail_link = lambda self: '<a target="_blank" href="%s">%s</a>'%(self.url,self.thumbnail)
  __unicode__ = lambda self: self.name

class PhotoModel(OrderedModel):
  photo = models.ForeignKey(Photo)
  slide_dimensions = "100x100"
  large_dimensions = "900x900"
  src = lambda self: self.photo.src
  __unicode__ = lambda self: str(self.photo)
  class Meta:
    abstract = True
