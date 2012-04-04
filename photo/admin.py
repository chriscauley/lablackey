from PIL import Image

from django.contrib import admin
from django import forms
from django.http import HttpResponse
from django.db.models.fields.files import FieldFile
from django.core.exceptions import ValidationError
from django.utils.html import escape, escapejs

from lablackey.photo.models import Photo

"""size_error = '''
    You must upload a photo/image as 4X3 (not smaller than 260 X 195
    pixels) or 3X4 (not smaller than 195 X 260 pixels).
    '''"""

class PhotoAdminForm(forms.ModelForm):
    class Meta:
        model = Photo
    def clean_src(self):
        src = self.cleaned_data['src']
        """if isinstance(src, FieldFile):
            image = Image.open(src)
            size_max = max(*image.size)
            size_min = min(*image.size)
            ratio = float(size_min) / size_max
            if size_max < 260 or ratio != 0.75:
                raise ValidationError(
                    size_error
                    + ' Size of uploaded image: %d X %d' % image.size)"""
        return src

class PhotoAdmin(admin.ModelAdmin):
    form = PhotoAdminForm
    list_display = (
        'id','name', 'thumbnail_', 'url', 'uploader', 'height_', 'width', 'type')
    fields = ('name', 'src')
    exclude = ['uploader']
    search_fields = ('name', 'src', 'uploader__username')

    def height_(self, photo):
        template = '%d<br/><span style="color: red">(%s)</span>'
        size_max = max(photo.height, photo.width)
        size_min = min(photo.height, photo.width)
        ratio = float(size_min) / size_max
        """if size_max < 260:
            return template % (photo.height, 'Too Small')
        elif ratio != 0.75:
            return template % (photo.height, 'Not 3X4 or 4X3')
        else:"""
        return photo.height
    height_.allow_tags = True

    def thumbnail_(self, photo):
        return photo.thumbnail_link_128x128
    thumbnail_.allow_tags = True

    def save_model(self, request, obj, form, change):
        if obj.uploader_id is None:
            obj.uploader = request.user
        obj.save()

    def response_add(self, request, obj, post_url_continue='../%s/'):
        if '_popup' in request.POST:
            from lablackey.photo.ajax_lookup import PhotoLookup
            pk_value = obj._get_pk_val()
            # opener.django.jQuery's trigger() method doesn't work quite
            # right, so opener.jQuery is used instead.
            return HttpResponse('''
                <script type="text/javascript">
                    (function($, window_name) {
                        var id = opener.windowname_to_id(window_name);
                        $('#' + id).trigger('didAddPopup', ['%s', '%s']);
                    })(opener.jQuery, window.name);
                    window.close();
                </script>
                ''' % (escape(pk_value),
                       escapejs(PhotoLookup().format_item(obj))))
        return super(PhotoAdmin, self).response_add(
                request, obj, post_url_continue)

admin.site.register(Photo, PhotoAdmin)
