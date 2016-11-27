from django.conf.urls import url

import views

urlpatterns = [
  url(r'^api/schema/([\w\d]+).([\w\d]+)/$',views.get_schema),
  url(r'^set_email/$',views.set_email ,name='set_email'),
  url(r'^api/login/$',views.login_ajax),
  url(r'^api/register/$',views.register_ajax),
  url(r'^user.json$',views.user_json),
  url(r'^accounts/logout/$',views.logout),
]
