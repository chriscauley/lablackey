from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import urls as auth_urls
from django.contrib.staticfiles.views import serve

from lablackey.decorators import resend_activation

admin.autodiscover()

import views, api

urlpatterns = [
  url(r'^api/schema/([\w\d]+).([\w\d]+Form)/$',views.get_form_schema),
  url(r'^api/schema/([\w\d]+).([\w\d]+)/$',views.get_schema),
  url(r'^form/([\w\d]+).([\w\d]+Form)/$',views.render_template,name="ur-form"),
  #url(r'^api/schema/([\w\d]+).([\w\d]+)/$',views.get_schema),
  url(r'^set_email/$',views.set_email ,name='set_email'),
  url(r'^user.json$',views.user_json),
  url(r'^accounts/logout/$',views.logout),
  url(r'^durf/([\w\d]+)/([\w\d]+)/$',api.get_many),
  url(r'^durf/([\w\d]+)/([\w\d]+)/(\d+)/$',api.get_one),
  url(r'favicon.ico$', views.redirect,
      {'url': getattr(settings,'FAVICON','/static/favicon.png')}),
  url(r'^admin/', include(admin.site.urls)),
  url(r'^auth/',include(auth_urls)),
  url(r'^$',views.render_template,kwargs={'template': "base.html"}),
]

if "social.apps.django_app.default" in settings.INSTALLED_APPS:
  import social.apps.django_app.urls
  urlpatterns.append(url('', include(social.apps.django_app.urls, namespace='social')))

if settings.DEBUG:
  from django.views.static import serve
  urlpatterns += [
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
  ]
