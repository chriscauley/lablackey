from django.conf.urls import url

import views

urlpatterns = [
  url(r'^api/schema/([\w\d]+).([\w\d]+)/$',views.get_schema),
]
