from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns(
    "lablackey.content.views",
    url(r"^([\w\d\-]*)/","page",name="page"),
)
