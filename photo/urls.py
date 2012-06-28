from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns(
  "photo.views",
  url(r'^add_photo_iframe/','photo.views.add_photo'),
)
