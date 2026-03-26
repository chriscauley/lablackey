from django.urls import re_path

from lablackey.sms import views

urlpatterns = [
  re_path(r"sms/add_phone/",views.add_phone),
  re_path(r"sms/verify_phone/",views.verify_phone),
  re_path(r"sms/delete_phone/",views.delete_phone),
]
