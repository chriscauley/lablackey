from django.urls import re_path

import lablackey.views
from . import views

urlpatterns = [
  re_path(r'^$', views.index, name="event_index"),
  re_path(r'^(\d+\-\d+\-\d+)/$', views.index, name="event_index"),
  re_path(r'^occurrence/(\d+)/$', views.occurrence_detail,name='occurrence_detail'),
  re_path(r'^(\d+)/(.+)/$', views.occurrence_detail,name='occurrence_detail'),
  re_path(r'ics/([^/]+)/([^/]+)/(\d+)/(.+).ics', views.ics,name="event_ics"),
  re_path(r'ics/(all_events).ics', views.all_ics,name="event_all_ics"),
  re_path(r'eventdetail_(\d+).json', views.detail_json),
  #re_path(r'weekly/(\d+\-\d+\-\d+)/', views.weekly,name="weekly"),
  #re_path(r'weekly/(\d+\-\d+\-\d+)/(?P<page_number>\d+)/',views.weekly,name="weekly"),
  #re_path(r'^(?P<page_number>\d+)/$', views.index, name="event_list"),
  #re_path(r'^tagged/(?P<slug>[^/]+)/(?P<page_number>\d+)/$', views.index, name="tagged"),
  re_path(r'^detail/(\d+)/(.+)/$', views.detail, name="event_detail"),
  re_path(r'^rsvp/$', views.rsvp, name='event_rsvp'),
  re_path(r'^checkin/$', views.checkin, name='event_rsvp'),
  re_path(r'^(own|disown)/(\d+)/',views.owner_ajax),
  re_path(r'^bulk.json$',views.bulk_ajax),

  re_path(r'^schedule/$',lablackey.views.single_page_app,name="conference"),
  re_path(r'^conference.json$',views.conference_json,name="conference.json"),
]
