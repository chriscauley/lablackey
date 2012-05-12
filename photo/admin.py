from PIL import Image

from django.contrib import admin
from django import forms
from django.http import HttpResponse
from django.db.models.fields.files import FieldFile
from django.core.exceptions import ValidationError
from django.utils.html import escape, escapejs

from lablackey.photo.models import Photo

class PhotoAdminForm(forms.ModelForm):
  class Meta:
    model = Photo

class PhotoAdmin(admin.ModelAdmin):
  form = PhotoAdminForm
  list_display = ('__unicode__', 'thumbnail_', 'uploader',)
  fields = ('title', 'src')
  exclude = ['uploader']
  search_fields = ('title', 'src', 'uploader__username')

  thumbnail_ = lambda self, photo: photo.thumbnail_link_128x128
  thumbnail_.allow_tags = True

  def save_model(self, request, obj, form, change):
    if obj.uploader_id is None:
      obj.uploader = request.user
    obj.save()

admin.site.register(Photo, PhotoAdmin)
