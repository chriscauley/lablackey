from django.conf import settings
from django.urls import re_path, include
from django.contrib import admin
from django.contrib.auth import urls as auth_urls
from django.contrib.staticfiles.views import serve
from django.db.utils import ProgrammingError

admin.autodiscover()

from . import views

urlpatterns = [
  #re_path(r'^api/schema/([\w\d]+).([\w\d]+)/$',views.get_schema),
  re_path(r'^set_email/$',views.set_email ,name='set_email'),
  re_path(r'^user.json$',views.user_json),
  re_path(r'^accounts/logout/$',views.logout),
  re_path(r'favicon.ico$', views.redirect,
      {'url': getattr(settings,'FAVICON','/static/favicon.png')}),
  re_path(r'^admin/', admin.site.urls),
  re_path(r'^$',views.render_template,kwargs={'template': "base.html"}),
  re_path(r'^auth/', include(auth_urls)),
  re_path(r'^auth/login/$',views.single_page_app,name="login"),
  re_path(r'^api/login/$',views.login_ajax,name='login_ajax'),
  re_path(r'^api/register/$',views.register_ajax,name='register_ajax'),
]

if 'lablackey.registration' in settings.INSTALLED_APPS:
  from lablackey.registration import urls as registration_urls
  urlpatterns += [
    re_path(r'^auth/',include(registration_urls)),
    re_path(r'^accounts/', include(registration_urls)),#! Depracated in favor of auth
  ]

if 'lablackey.api' in settings.INSTALLED_APPS:
  from lablackey.api import views as api_views
  from lablackey.api.urls import build_urls
  urlpatterns += [
    re_path(r'^durf/([\w\d]+)/([\w\d]+)/$',api_views.get_many),
    re_path(r'^durf/([\w\d]+)/([\w\d]+)/(\d+)/$',api_views.get_one),
    re_path(r'^api/schema/([\w\d\.]+)\.([\w\d]+Form)/$',views.get_form_schema,name="ur_form_add"),
    re_path(r'^api/schema/([\w\d\.]+)\.([\w\d]+Form)/(\d+)/$',views.get_form_schema,name="ur_form_schema"),
    re_path(r'^api/schema/([\w\d]+)\.([\w\d]+)/$',views.get_schema),
    re_path(r'^form/([\w\d\.]+)([\w\d]+Form)/$',views.render_template,name="ur-form"),
  ]
  urlpatterns += build_urls()
  if settings.DEBUG:
    import lablackey.dummy.views as dummy_views
    urlpatterns += [
      re_path(r'^api/test/reset/$',dummy_views.reset)
    ]

if 'social_django' in settings.INSTALLED_APPS: # django companion app for python-social-auth
  import social_django.urls
  urlpatterns.append(re_path('', include(social_django.urls, namespace='social')))

if "social.apps.django_app.default" in settings.INSTALLED_APPS: # older version of python-social-auth
  import social.apps.django_app.urls
  urlpatterns.append(re_path('', include(social.apps.django_app.urls, namespace='social')))

if 'lablackey.blog' in settings.INSTALLED_APPS:
  import lablackey.blog.urls
  urlpatterns.append(re_path(r'^blog/',include(lablackey.blog.urls)))

if 'airbrake' in settings.INSTALLED_APPS: # django-airbreak-lite
  import airbrake.urls
  urlpatterns.append(re_path(r'',include(airbrake.urls)))

#! TODO: django.contrib.flatpages.middleware.FlatpageFallbackMiddleware looks preferable
if 'django.contrib.flatpages' in settings.INSTALLED_APPS:
  from django.contrib.flatpages.models import FlatPage
  import django.contrib.flatpages.views
  # this breaks on initial migration before flatpages are migrated
  try:
    fps = '|'.join([page.url[1:] for page in FlatPage.objects.all()])
    urlpatterns.append(re_path(r'^(%s)$'%fps,django.contrib.flatpages.views.flatpage,name='flatpage'))
  except ProgrammingError:
    pass

if settings.DEBUG:
  from django.views.static import serve
  urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
  ]
