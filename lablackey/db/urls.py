from django.urls import re_path

from . import views

urlpatterns = [
  re_path('^admin/merge_model/(.*)/(.*)/$',views.merge_model)
]
