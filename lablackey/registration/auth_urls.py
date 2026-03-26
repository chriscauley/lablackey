from django.urls import re_path

import django.contrib.auth.views as auth_views

urlpatterns = [
  re_path(r'^login/$',auth_views.LoginView.as_view(template_name='registration/login.html'),
      name='auth_login'),
  re_path(r'^logout/$',auth_views.LogoutView.as_view(template_name='registration/logout.html'),
      name='auth_logout'),
  re_path(r'^password/change/$',auth_views.PasswordChangeView.as_view(),name='auth_password_change'),
  re_path(r'^password/change/done/$',auth_views.PasswordChangeDoneView.as_view(),
      name='auth_password_change_done'),
  re_path(r'^password/reset/$',auth_views.PasswordResetView.as_view(),name='auth_password_reset'),
  re_path(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
      auth_views.PasswordResetConfirmView.as_view(),name='auth_password_reset_confirm'),
  re_path(r'^password/reset/complete/$',auth_views.PasswordResetCompleteView.as_view(),
      name='auth_password_reset_complete'),
  re_path(r'^password/reset/done/$',auth_views.PasswordResetDoneView.as_view(),
      name='auth_password_reset_done'),
]
