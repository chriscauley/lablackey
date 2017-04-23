from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect

from lablackey.mail import send_template_email

import urllib2

def auth_required(func, **decorator_kwargs):
  # kwargs can be redirect_field_name and login_url (see login_required)
  def wrapper(request, *args, **kwargs):
    user=request.user  
    if request.user.is_authenticated():
      return func(request, *args, **kwargs)
    if request.is_ajax():
      response = JsonResponse({'error': "You must be logged in to continue"},status=401)
      response['WWW-Authenticate'] = 'Basic realm="api"'
      return response
    return login_required(func)(request,**decorator_kwargs)
  wrapper.__doc__ = func.__doc__
  wrapper.__name__ = func.__name__
  return wrapper

def email_required(func):
  def wrap(request, *args, **kwargs):
    if not request.user.is_authenticated():
      return auth_required(func)(request,**kwargs)
    if not request.user.email:
      return HttpResponseRedirect("/set_email/?next=%s"%urllib2.quote(request.path))
    return func(request, *args, **kwargs)
  wrap.__doc__=func.__doc__
  wrap.__name__=func.__name__
  return wrap

def cached_method(target,name=None):
  target.__name__ = name or target.__name__
  if target.__name__ == "<lambda>":
    raise ValueError("Using lambda functions in cached_methods causes __name__ collisions.")
  def wrapper(*args, **kwargs):
    obj = args[0]
    name = '___' + target.__name__

    if not hasattr(obj, name):
      value = target(*args, **kwargs)
      setattr(obj, name, value)
        
    return getattr(obj, name)
      
  return wrapper

def cached_property(target,name=None):
  return property(cached_method(target,name=name))

def activate_user(target):
  def wrapper(request,*args,**kwargs):
    data = request.POST or request.GET
    model = get_user_model()
    if data.get('email',None):
      try:
        if hasattr(model.objects,"keyword_search"):
          user = model.objects.keyword_search(data.get('email'))[0]
        else:
          user = model.objects.get(email=data.get("email"))
        user.is_active = True
        user.save()
      except (model.DoesNotExist,IndexError):
        send_template_email("email/no_user",[data.get("email")],context={})
    return target(request,*args,**kwargs)
  return wrapper
