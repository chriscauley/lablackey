from django.http import HttpResponse, HttpResponseRedirect
from django.core import urlresolvers
from django.db import models
from django import forms

class TinyMCE(object):
  class Media:
    js = [
      'gmedia/tinymce/jscripts/tiny_mce/tiny_mce.js',
      'js/tinymce_setup.js'
      ]
