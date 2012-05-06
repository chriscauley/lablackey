from django.contrib import admin
from django import forms
from lablackey.content.models import Page,Copy, ListItem, ItemList, DesignImage
from lablackey.content.mixins import CKEditorMixin

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

class ListItemInline(admin.TabularInline):
    model = ListItem
    extra = 0
    optional_fields = ('order','last_name','url','logo','description', )
    _readonly_fields = ("order",)
    def get_readonly_fields(self,request,obj=None):
        if ItemList.objects.get(id=request.path.split("/")[-2]).show_order:
            return ()
        return self._readonly_fields
    def get_fieldsets(self,request,obj=None):
        fields = ["name"]
        il = ItemList.objects.get(id=request.path.split("/")[-2])
        for f in self.optional_fields:
            if getattr(il,"show_"+f):
                fields.append(f)
        return ((None,{"fields": fields}),)
        
class ItemListForm(forms.ModelForm):
    model = ListItem
    class Media:
        css = { "all": ("design/content-admin.css",) }

class ItemListAdmin(admin.ModelAdmin):
    form = ItemListForm
    _list_editable = ('columns','context',"show_logo","show_url","show_order","show_description","show_last_name")
    _readonly_fields = ("name","page","columns","context","show_logo","show_url",
                        "show_description","show_last_name","show_order")
    inlines = [ ListItemInline ]
    def get_fieldsets(self,request,obj=None):
        if request.user.is_superuser:
            return ((None,
                    {'fields':
                         (("name","context"),("columns","page"),
                          ("show_logo","show_url","show_order"),("show_description","show_last_name"))}),)
        return ((None,{'fields': ("name",)}),)
    def get_readonly_fields(self,request,obj=None):
        if request.user.is_superuser: return ()
        return self._readonly_fields
    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            if not "columns" in self.list_display:
                self.list_display.extend(self._list_editable)
            self.exclude = ()
            self.list_editable = self._list_editable
        else:
            self.exclude = self._list_editable
            self.list_editable = ()
            self.list_display = self.list_display[:2] #really don't like this line

        return super(ItemListAdmin, self).changelist_view(request, extra_context)
    def has_add_permission(self, request):
        return request.user.is_superuser

class DesignImageAdmin(PageContentModelAdmin):
    model = DesignImage

admin.site.register(Page)
admin.site.register(Copy,CopyAdmin)
admin.site.register(ItemList,ItemListAdmin)
admin.site.register(DesignImage,DesignImageAdmin)
