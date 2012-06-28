from django.db import models
from sorl.thumbnail import ImageField, get_thumbnail
from mwm.db.models import OrderedModel

class Photo(models.Model):
  name = models.CharField(max_length=512)
  src = ImageField(upload_to='uploads/photos/%Y-%m',max_length=300)

  thumbnail = lambda self:'<img src="%s"/>'%(get_thumbnail(self.src, '128x128').url)
  thumbnail_link = lambda self: '<a target="_blank" href="%s">%s</a>'%(self.url,self.thumbnail)
  __unicode__ = lambda self: self.name

class PhotoModel(OrderedModel):
  photo = models.ForeignKey(Photo)
  slide_dimensions = "100x100"
  large_dimensions = "900x900"
  __unicode__ = lambda self: str(self.photo)
  class Meta:
    abstract = True
