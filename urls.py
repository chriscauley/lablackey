# note that this is just a tupl and does nothing on its own
# this is intended to be splatted into patterns
llpatterns = (
    'lablackey',
    (r'^login','views.login'),
    (r'^logout','ezgauth.logout'),
)
