from django.contrib import admin
from django import forms
from lablackey.content.mixins import CKEditorMixin
from lablackey.content.models import Page, Copy, DesignImage, Section, Page, PageImage
from lablackey.db.admin import OrderedAdmin

class PageContentModelAdmin(admin.ModelAdmin):
  exclude = ('context',)
  def changelist_view(self, request, extra_context=None):
    if request.user.is_superuser:
      #this conditional is needed or columns duplicate linearly
      if not "context" in self.list_display:
        self.list_display.extend(["context"])
        self.list_editable = ("context",)
    return super(PageContentModelAdmin, self).changelist_view(request, extra_context)
  def has_add_permission(self, request):
    return request.user.is_superuser

class CopyAdmin(CKEditorMixin,PageContentModelAdmin):
  list_filter =("page",)
  list_display = ("page","name","text")
  list_display_links = ("name",)
  exclude = ("context","page")
  readonly_fields = ("name","text")

class CopyInline(CKEditorMixin, admin.StackedInline):
  model = Copy
  has_add_permission = lambda self,request: False
  exclude = ('context',)
  extra = 0

class DesignImageAdmin(PageContentModelAdmin):
  model = DesignImage

class PageImageForm(forms.ModelForm):
  order = forms.IntegerField(widget=forms.HiddenInput)
  class Meta:
    model = PageImage

class SectionForm(forms.ModelForm):
  order = forms.IntegerField(widget=forms.HiddenInput)
  class Meta:
    model = Section

class CarouselItemAdmin(OrderedAdmin):
  fields = ("order",'title','photo','thumbnail_')
  readonly_fields = ('thumbnail_',)
  list_display = OrderedAdmin.list_display + ('thumbnail_',)
  raw_id_fields = ("photo",)

class PageImageInline(admin.TabularInline):
  sortable_field_name = "order"
  model = PageImage
  fields = ('page','photo','caption_override','edit','order')
  readonly_fields = ("edit",)
  extra = 0
  raw_id_fields = ("photo",)
  form = PageImageForm

class SectionInline(CKEditorMixin,admin.StackedInline):
  model = Section
  #verbose_name_plural = "Section on the page."
  fieldsets = (
    (None,
     {"fields":('page',"title",'hide_title',"body","order")}
     ),
    )
  extra = 2
  #sortable_field_name = "order"
  #form = SectionForm

class PageAdmin(admin.ModelAdmin):
  exclude = ('slug',)
  inlines = [PageImageInline, SectionInline,CopyInline]
  has_add_permission = lambda self,request: False

admin.site.register(Copy,CopyAdmin)
admin.site.register(DesignImage,DesignImageAdmin)
admin.site.register(Page,PageAdmin)
