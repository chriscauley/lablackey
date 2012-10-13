from django.contrib import admin
from .models import Page, Copy, DesignImage, HouseAd, Template, SideBarWidget, TextArea
from lablackey.db.admin import OrderedModelInline

class PageContentInline(admin.TabularInline):
  exclude = ('context',)
  #readonly_fields = ('name',)
  has_add_permission = lambda self, request: False
  #has_delete_permission = lambda self, request, obj: request.user.is_superuser

class CopyInline(PageContentInline):
  fields = ('name','text')
  model = Copy

class TextAreaInline(PageContentInline):
  fields = ('name','text')
  model = TextArea

class DesignImageInline(PageContentInline):
  fields = ('src','name')
  model = DesignImage

class HouseAdInline(admin.TabularInline):
  model = HouseAd
  extra = 0

class TemplateAdmin(admin.ModelAdmin):
  pass

class SideBarWidgetInline(OrderedModelInline):
  model = SideBarWidget
  extra = 0

class PageAdmin(admin.ModelAdmin):
  readonly_fields = ('name',)
  inlines = [CopyInline,DesignImageInline,TextAreaInline] #,HouseAdInline,SideBarWidgetInline]

admin.site.register(Page,PageAdmin)
admin.site.register(Template,TemplateAdmin)
