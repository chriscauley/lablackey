from django.http import HttpResponse, HttpResponseRedirect
from django.core import urlresolvers
from django.db import models
from django import forms

class CKEditorMixin(object):
  """Changes widget for all TextFields to use CKEditor."""
  formfield_overrides = {
    models.TextField: { 'widget': forms.Textarea(attrs={'class': 'ckeditor'}), },
    }

  class Media:
    js = ['ckeditor/ckeditor.js']
