from django.contrib.auth.decorators import login_required


def auth_required(function, **decorator_kwargs):
  # kwargs can be redirect_field_name and login_url (see login_required)
  def wrapper(request, *args, **kwargs):
    user=request.user  
    if request.user.is_authenticated():
      return function(request, *args, **kwargs)
    if request.is_ajax():
      response = JsonResponse({'error': "You must be logged in to continue"},status=401)
      response['WWW-Authenticate'] = 'Basic realm="api"'
      return response
    return login_required(request,**decorator_kwargs)
  wrapper.__doc__ = function.__doc__
  wrapper.__name__ = function.__name__
  return wrapper
