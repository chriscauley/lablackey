from django.http import HttpResponse, HttpResponseRedirect
from django.core import urlresolvers
from django.db import models
from django import forms


class CKEditorMixin(object):
  """Changes widget for all TextFields to use CKEditor."""
  formfield_overrides = {
    models.TextField: {
      'widget': forms.Textarea(attrs={'class': 'ckeditor'}),
      },
    }

  class Media:
    js = [
      'js/jquery-1.7.1.min.js',
      'ckeditor/ckeditor.js',
      'ckeditor/config.js',
      ]

class TinyMCE(object):
  class Media:
    js = [
      'gmedia/tinymce/jscripts/tiny_mce/tiny_mce.js',
      'js/tinymce_setup.js'
      ]
