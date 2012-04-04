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
        js = ['ckeditor/ckeditor.js']


class ChampionshipDependentMixin(object):
    """Mixin for the ModelAdmin subclasses for Section and Page.

    If the Section or Page change-form is opened in a popup, that window
    is just closed. If they are not opened in a popup, the user is
    redirected to the championship it belongs to.
    """

    def response_change(self, request, obj):
        default = super(ChampionshipDependentMixin, self).response_change(
            request, obj)
        if "_popup" in request.POST:
            return HttpResponse(
                '<script type="text/javascript">'
                'window.close();'
                '</script>')
        # Redirect to championship.
        if getattr(self, 'championship', None) is not None:
            change_url = urlresolvers.reverse(
                'admin:content_championship_change',
                args=[self.championship.id],
                current_app=self.admin_site.name)
            return HttpResponseRedirect(request.get_full_path())
        return default


class ChampionshipIndependentMixin(object):
    """Mixin for the ModelAdmin subclasses for Event, Map, and Place.

    If the Event, Map, or Place change-form is opened in a popup, that
    window is just closed. If they are not opened in a popup, the user
    is redirected to the normal list of items.
    """

    def response_change(self, request, obj):
        default = super(ChampionshipIndependentMixin, self).response_change(
            request, obj)
        if "_popup" in request.POST:
            return HttpResponse(
                '<script type="text/javascript">'
                'window.close();'
                '</script>')
        return default
