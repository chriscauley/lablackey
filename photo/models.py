from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from PIL import Image
import sorl.thumbnail

class Photo(models.Model):
    title = models.CharField(max_length=64)
    src = sorl.thumbnail.ImageField('Image', max_length=300,upload_to='photos/%Y-%m')
    uploader = models.ForeignKey(User, verbose_name="Uploaded By")
    caption = models.CharField(max_length=256,null=True,blank=True)

    __unicode__ = lambda self: self.title

    @property
    def thumbnail_img_128x128(self):
        im = sorl.thumbnail.get_thumbnail(self.src, '128x128', quality=70)
        return '<img src="%s"/>' % (im.url,)

    @property
    def thumbnail_link_128x128(self):
        return '<a target="_blank" href="%s">%s</a>' % (self.url, self.thumbnail_img_128x128)
