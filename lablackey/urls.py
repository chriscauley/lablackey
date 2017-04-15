from django.conf import settings
from django.conf.urls import url

import views, api

urlpatterns = [
  url(r'^api/schema/([\w\d]+).([\w\d]+Form)/$',views.get_form_schema),
  url(r'^api/schema/([\w\d]+).([\w\d]+)/$',views.get_schema),
  url(r'^set_email/$',views.set_email ,name='set_email'),
  url(r'^api/login/$',views.login_ajax,name='login'),
  url(r'^api/register/$',views.register_ajax),
  url(r'^user.json$',views.user_json),
  url(r'^accounts/logout/$',views.logout),
  url(r'^durf/([\w\d]+)/([\w\d]+)/$',api.get_many),
  url(r'^durf/([\w\d]+)/([\w\d]+)/(\d+)/$',api.get_one),
  url(r'favicon.ico$', main_views.redirect,
      {'url': getattr(settings,'FAVICON','/static/favicon.png')}),
]

if settings.DEBUG:
  from django.views.static import serve
  urlpatterns += [
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
  ]
