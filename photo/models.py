from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from PIL import Image
import sorl.thumbnail

class Photo(models.Model):
    name = models.CharField(max_length=64)
    src = sorl.thumbnail.ImageField(
        'Image', max_length=300,
        upload_to=settings.UPLOAD_DIR + '/photos/%Y-%m')
    uploader = models.ForeignKey(User, verbose_name="Uploaded By")
    caption = models.CharField(max_length=256,null=True,blank=True)

    def __init__(self, *args, **kw):
        super(Photo, self).__init__(*args, **kw)
        self._pil_cache = None

    @property
    def pil_cache(self):
        if self._pil_cache is None:
            image = Image.open(self.src)
            self._pil_cache = dict(width=image.size[0],height=image.size[1],
                                   type=image.format)
        return self._pil_cache

    @property
    def type(self): return self.pil_cache['type']
    @property
    def width(self): return self.pil_cache['width']
    @property
    def height(self): return self.pil_cache['height']
    @property
    def url(self): return settings.MEDIA_URL + self.src.name

    def __unicode__(self):
        return self.name

    @property
    def thumbnail_img_128x128(self):
        im = sorl.thumbnail.get_thumbnail(self.src, '128x128', quality=70)
        return '<img src="%s"/>' % (im.url,)

    @property
    def thumbnail_link_128x128(self):
        return '<a target="_blank" href="%s">%s</a>' % (self.url, self.thumbnail_img_128x128)

class PhotoSetModel(models.Model):
    images = models.ManyToManyField(Photo,blank=True)
    @property
    def first_image(self):
        result = self.images.all()[:1]
        if len(result) == 0:
            return None
        else:
            return result[0]
    class Meta:
        abstract = True
