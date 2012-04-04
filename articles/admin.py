from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from forms import ArticleAdminForm
from models import Tag, Article, Attachment
from lablackey.content.admin_mixins import CKEditorMixin

def article_auth(user):
    groups = [str(g) for g in user.groups.all()]
    return user.is_superuser or "Superuser" in groups

class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1
    max_num = 15

class ArticleAdmin(CKEditorMixin, admin.ModelAdmin):
    list_display = ['title',  'author', 'publish_date']
    list_filter = ['author',]
    _list_editable = ['is_live']
    list_per_page = 25
    search_fields = ('title', 'keywords', 'description', 'content')
    date_hierarchy = 'publish_date'
    form = ArticleAdminForm
    inlines = [
        AttachmentInline,
    ]

    fieldsets = (
        (None, {'fields': ( 'title','content','tags','auto_tag','images')}),
        ('Metadata', {'fields': ('slug','description'),
                      'classes': ('collapse',),}),
        ('Scheduling', {'fields': ('publish_date',)}),
    )

    filter_horizontal = ('tags', 'followup_for', 'related_articles')
    prepopulated_fields = {'slug': ('title',)}

    """def get_fieldsets(self,request,obj=None):
        if request.user.is_superuser:
            return ((None,
                    {'fields':
                         (("name","context"),("columns","page"),
                          ("show_logo","show_url","show_order"),("show_description","show_last_name"))}),)
        return ((None,{'fields': ("name",)}),)
    def get_readonly_fields(self,request,obj=None):
        if request.user.is_superuser: return ()
        return self._readonly_fields"""
    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            if not "is_live" in self.list_display:
                self.list_display.extend(self._list_editable)
            self.exclude = ()
            self.list_editable = self._list_editable
        else:
            self.exclude = self._list_editable
            self.list_editable = ()
        return super(ArticleAdmin, self).changelist_view(request, extra_context)
    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
    mark_active.short_description = _('Mark select articles as active')

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
    mark_inactive.short_description = _('Mark select articles as inactive')

    def save_model(self, request, obj, form, change):
        """Set the article's author based on the logged in user
        and make sure at least one site is selected
        """
        if obj.author.id ==1:
            obj.author = request.user
        obj.save()

        # this requires an Article object already
        obj.do_auto_tag('default')
        if 'tags' in form.cleaned_data:
            form.cleaned_data['tags'] += list(obj.tags.all())

    def queryset(self, request):
        """Limit the list of articles to article posted
        by this user unless they're a superuser.
        """
        groups = [str(g) for g in request.user.groups.all()]
        if request.user.is_superuser or "Superuser" in groups:
            return self.model._default_manager.all()
        else:
            return self.model._default_manager.filter(author=request.user)

admin.site.register(Tag)
admin.site.register(Article, ArticleAdmin)
