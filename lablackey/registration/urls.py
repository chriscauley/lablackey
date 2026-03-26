from django.conf import settings
from django.urls import re_path, include
from django.contrib.auth import get_user_model
from django.views.generic.base import TemplateView
from django.utils import timezone

from . import views, auth_urls
import datetime
from lablackey.decorators import resend_activation
import lablackey.views

urlpatterns = [
  re_path(r'^register/$',lablackey.views.single_page_app,name="register"),
  re_path(r'^register/complete/$',lablackey.views.render_template,kwargs={"template":"registration/complete.html"},
      name='registration_complete'),
  re_path(r'^register/(\w+)/$',views.activate,name='registration_activate'),
  re_path(r'^activate/(\w+)/$',views.activate), #! DEPRACATED in favor of the above
]
