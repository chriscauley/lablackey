from django.conf.urls import url

from lablackey.sms import views

urlpatterns = [
  url(r"sms/add_phone/",views.add_phone),
  url(r"sms/verify_phone/",views.verify_phone),
  url(r"sms/delete_phone/",views.delete_phone),
]
