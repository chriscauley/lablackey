"""
For an "image" ForeignKey attribute referencing the Photo model class,
your admin class' form class can inherit from PhotoForeignKeyForm or
RequiredPhotoForeignKeyForm, when the "image" field cannot be null.

For an "images" ManyToManyField, you can have your admin class' form
class inherit from PhotoManyToManyForm.
"""
from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from ajax_select.fields import (
    AutoCompleteSelectField, AutoCompleteSelectMultipleField,
    AutoCompleteSelectWidget, AutoCompleteSelectMultipleWidget)


class PhotoWidgetMixin(object):

    def render(self, name, value, attrs=None):
        output = []
        output.append(
            super(PhotoWidgetMixin, self).render(name, value, attrs))
        related_url = reverse('admin:photo_photo_add')
        output.append(
            u'<a href="%s" id="add_id_%s" '
            u'onclick="return showAddAnotherPopup(this);"> ' % (
                related_url, name))
        output.append(
            u'<img src="%simg/admin/icon_addlink.gif" width="10" '
            u'height="10"/> Upload Photo</a>' % settings.ADMIN_MEDIA_PREFIX)
        return mark_safe(u''.join(output))


class PhotoAutoCompleteWidget(PhotoWidgetMixin, AutoCompleteSelectWidget):
    """Photo ForeignKey autocomplete widget with 'Upload Photo' link."""


class PhotoAutoCompleteMultipleWidget(PhotoWidgetMixin,
                                      AutoCompleteSelectMultipleWidget):
    """Photo ManyToMany autocomplete widget with 'Upload Photo' link."""


class PhotoAutoCompleteSelectMultipleField(AutoCompleteSelectMultipleField):

    def __init__(self, channel, *args, **kwargs):
        self.channel = channel
        # Don't call super(PhotoAutoCompleteSelectMultipleField).__init__()
        # because AutoCompleteSelectMultipleField.__init__() overrides
        # kwargs['widget'].
        super(AutoCompleteSelectMultipleField, self).__init__(*args, **kwargs)


class PhotoFormBase(forms.ModelForm):

    class Media:
        css = {
            'all': [
                # Autocomplete widget.
                'jquery/jquery.autocomplete.css',
                'ajax_select/iconic.css',
                ],
            }
        js = [
            # Autocomplete widget.
            'jquery/jquery-1.5.min.js',
            'jquery/jquery.autocomplete.js',
            'ajax_select/ajax_select.js',
            ]


class PhotoForeignKeyForm(PhotoFormBase):

    # See the photo.ajax_lookup.PhotoLookup class.
    _channel = 'photo'
    _help_text = 'Search for photo'
    image = AutoCompleteSelectField(
        channel=_channel, label='Image', required=False,
        widget=PhotoAutoCompleteWidget(_channel, _help_text),
        help_text=_help_text)


class RequiredPhotoForeignKeyForm(PhotoFormBase):

    # See the photo.ajax_lookup.PhotoLookup class.
    _channel = 'photo'
    _help_text = 'Search for photo'
    image = AutoCompleteSelectField(
        channel=_channel, label='Image', required=True,
        widget=PhotoAutoCompleteWidget(_channel, _help_text),
        help_text=_help_text)


class PhotoManyToManyForm(PhotoFormBase):

    # See the photo.ajax_lookup.PhotoLookup class.
    _channel = 'photo'
    _help_text = 'Search for photos'
    images = PhotoAutoCompleteSelectMultipleField(
        channel=_channel, label='Images', required=False,
        widget=PhotoAutoCompleteMultipleWidget(_channel, _help_text),
        help_text=_help_text)
