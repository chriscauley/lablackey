from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from crop_override.admin import CropAdmin
from sorl.thumbnail import get_thumbnail

from .models import Post, Banner, PressItem
from .forms import PostForm

from lablackey.db.admin import RawMixin
from lablackey.db.forms import StaffMemberForm
from wmd.widgets import AdminMarkDownInput

class PostAdminForm(PostForm):
  """ Just like post form, but with user """
  exclude = ('slug',)
  class Meta:
    model = Post
    fields = ('user','title','slug','content','short_content','publish_dt','tags','status','photo')

class PostAdmin(RawMixin,admin.ModelAdmin):
  form = PostAdminForm
  list_display = ('__unicode__','user','featured','publish_dt','status')
  list_editable = ('featured','status')
  search_fields = ('content',)
  raw_id_fields = ('photo','user')

admin.site.register(Post,PostAdmin)
admin.site.register(PressItem)
#admin.site.register(Banner)

if 'django.contrib.flatpages' in settings.INSTALLED_APPS:
  from django.contrib.flatpages.models import FlatPage
  from django.contrib.flatpages.admin import FlatPageAdmin
  from django.contrib.flatpages.forms import *
  from django.contrib import messages

  from media.admin import TaggedPhotoInline

  admin.site.unregister(FlatPage)

  TEMPLATE_CHOICES = (
      ('','HTML'),
      ('flatpages/markdown.html','MarkDown'),
    )

  class FlatPageForm(forms.ModelForm):
    template_name = forms.CharField(label="Render As",help_text="",required=False,initial="flatpages/markdown.html")
    def __init__(self, *args, **kwargs):
      super(FlatPageForm, self).__init__(*args, **kwargs)
      self.fields['template_name'].widget = forms.Select(choices=TEMPLATE_CHOICES)
      self.fields['content'].widget = AdminMarkDownInput()
    class Meta:
      model = FlatPage
      exclude = ()

  class FlatPageAdmin(FlatPageAdmin):
    list_display = ('url','title','template_name')
    form = FlatPageForm
    #inlines = [TaggedPhotoInline]
    def save_model(self, request, obj, form, change):
      old_url = obj.url
      super(FlatPageAdmin, self).save_model(request, obj, form, change)
      obj = self.model.objects.get(id=obj.id)
      if old_url != obj:
        messages.error(request,"The url of this page has been changed. This will not update unless the server is reset. Please contact the administrator")
  admin.site.register(FlatPage,FlatPageAdmin)
