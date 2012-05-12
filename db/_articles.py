import logging

from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django import forms
from lablackey.content.mixins import CKEditorMixin
from articles.forms import ArticleAdminForm
from articles.admin import ArticleAdmin
from articles.models import Tag, Article, ArticleStatus, Attachment
#from .models import ArticlePhoto # not implimented

log = logging.getLogger('articles.admin')

class TagAdmin(admin.ModelAdmin):
  list_display = ('name', 'article_count')

  def article_count(self, obj):
    return obj.article_set.count()
  article_count.short_description = _('Applied To')

"""class ArticlePhotoForm(forms.ModelForm):
  order = forms.IntegerField(widget=forms.HiddenInput)
  class Meta:
    model = ArticlePhoto

class ArticlePhotoInline(admin.TabularInline):
  model = ArticlePhoto
  form = ArticlePhotoForm
  fields = ("name","src","order")
  sortable_field_name = "order" """

class ArticleAdmin(CKEditorMixin,ArticleAdmin):
  list_display = ('title', 'status', 'author', 'publish_date')
  list_filter = ('author', 'status', 'is_active')
  list_per_page = 25
  search_fields = ('title', 'keywords', 'description', 'content')
  form = ArticleAdminForm

  fieldsets = (
    (None,
     {'fields': ('title', 'content', 'tags', 'auto_tag', 'status','publish_date')}
     ),
    ('Metadata', 
     {'fields': ('description',), 'classes': ('collapse',) }
     ),
    #('Relationships', {
    #  'fields': ('followup_for', 'related_articles'),
    #  'classes': ('collapse',)
    #}),
    #('Scheduling', {'fields': ('publish_date', 'expiration_date')}),
    #('AddThis Button Options', {
    #  'fields': ('use_addthis_button', 'addthis_use_author', 'addthis_username'),
    #  'classes': ('collapse',)
    #}),
    ('Advanced', {
      'fields': ('slug', 'is_active'),
      'classes': ('collapse',)
    }),
  )
  filter_horizontal = ('tags', 'followup_for', 'related_articles')
  """
  prepopulated_fields = {'slug': ('title',)}

  def tag_count(self, obj):
    return str(obj.tags.count())
  tag_count.short_description = _('Tags')

  def mark_active(self, request, queryset):
    queryset.update(is_active=True)
  mark_active.short_description = _('Mark select articles as active')

  def mark_inactive(self, request, queryset):
    queryset.update(is_active=False)
  mark_inactive.short_description = _('Mark select articles as inactive')

  def get_actions(self, request):
    actions = super(ArticleAdmin, self).get_actions(request)

    def dynamic_status(name, status):
      def status_func(self, request, queryset):
        queryset.update(status=status)

      status_func.__name__ = name
      status_func.short_description = _('Set status of selected to "%s"' % status)
      return status_func

    for status in ArticleStatus.objects.all():
      name = 'mark_status_%i' % status.id
      actions[name] = (dynamic_status(name, status), name, _('Set status of selected to "%s"' % status))

    def dynamic_tag(name, tag):
      def status_func(self, request, queryset):
        for article in queryset.iterator():
          log.debug('Dynamic tagging: applying Tag "%s" to Article "%s"' % (tag, article))
          article.tags.add(tag)
          article.save()

      status_func.__name__ = name
      status_func.short_description = _('Apply tag "%s" to selected articles' % tag)
      return status_func

    for tag in Tag.objects.all():
      name = 'apply_tag_%s' % tag.pk
      actions[name] = (dynamic_tag(name, tag), name, _('Apply Tag: %s' % (tag.slug,)))

    return actions

  actions = [mark_active, mark_inactive]"""


admin.site.unregister(Tag)
admin.site.register(Tag, TagAdmin)
admin.site.unregister(Article)
admin.site.register(Article, ArticleAdmin)
admin.site.unregister(ArticleStatus)
