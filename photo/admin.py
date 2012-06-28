from django.contrib import admin
from mwm.db.admin import OrderedModelInline
from mwm.photo.models import Photo

class PhotoAdmin(admin.ModelAdmin):
  list_display = ('name', 'thumbnail_')
  thumbnail_ = lambda self, photo: photo.thumbnail()
  thumbnail_.allow_tags = True

class PhotoModelInline(OrderedModelInline):
  extra = 0
  raw_id_fields = ("photo",)

admin.site.register(Photo, PhotoAdmin)
