from django.contrib import admin
from lablackey.db.admin import OrderedModelInline
from lablackey.photo.models import Photo
from crop_override.admin import CropAdmin

class PhotoAdmin(CropAdmin):
  list_display = ('name', 'thumbnail_')
  thumbnail_ = lambda self, photo: photo.thumbnail()
  thumbnail_.allow_tags = True

class PhotoModelInline(OrderedModelInline):
  extra = 0
  raw_id_fields = ("photo",)

admin.site.register(Photo, PhotoAdmin)
