from django.http import HttpResponseRedirect
from ezgauth import check_login

@check_login
def login(request):
    return HttpResponseRedirect(getattr("next",request.GET,"/"))
