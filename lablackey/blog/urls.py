from django.urls import re_path
from django.contrib.sitemaps import views as sitemaps_views
from django.http import HttpResponse

from . import views

username_regex = '([\w\d\-\.\@\_]+)'

urlpatterns = [
  re_path(r'^admin/add/$', views.edit, name="add"),
  re_path(r'^admin/edit/(?P<pk>\d+)/$', views.edit, name="edit"),
  re_path(r'^admin/delete/(?P<pk>\d+)/$', views.delete, name="delete"),
  re_path(r'^admin/drafts/$', views.drafts, name="drafts"),
  re_path(r'^admin/preview/$', views.render_preview, name="render_preview"),

  re_path(r'^tag/(.+)/$', views.posts_by_tag,name='posts_by_tag'),
  re_path(r'^(\d+)/([\w\d\-]+)/$', views.post_detail, name="post_detail"),
  re_path(r'^%s/([\w\d\-]+)/$'%username_regex, views.post_detail, name="post_detail"),
  re_path(r'^%s/$'%username_regex, views.post_list, name="post_list"),
  re_path(r'^$', views.home,name="blog_home"),
]
