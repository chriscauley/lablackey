from django.conf import settings
from django.contrib.auth import authenticate, login, logout as _logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.db.models import Q
from django import forms
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

import json, random

def login_ajax(request):
  if not ('username' in request.POST and 'password' in request.POST):
    return JsonReponse({ 'errors': { 'non_field_errors': ['Please enter username and password'] } })
  user = authenticate(username=request.POST['username'],password=request.POST['password'])
  if not user:
    return JsonResponse({ 'errors': { 'non_field_errors': ['Username and password do not match.'] } })
  login(request,user)
  return JsonResponse({ 'user': {'id': user.id, 'username': user.username, 'email': user.email } })

def user_json(request):
  user = request.user
  if user.is_authenticated():
    return JsonResponse({ 'user': {'id': user.id, 'username': user.username, 'email': user.email } })
  return JsonResponse({})

def logout(request):
  _logout(request)
  return HttpResponseRedirect("/")

def robots(request):
  if settings.DEBUG:
    return HttpResponse("User-agent: *\nDisallow: /")
  return HttpResponse("")

def register_ajax(request):
  User = get_user_model()
  email = request.POST.get('email',None)
  _Q = Q(email=email)|Q(username=email)
  for f in getattr(settings,"EXTRA_AUTH_FIELDS",[]):
    _Q = _Q | Q(**{f:email})
  matching_users = list(User.objects.filter(_Q))
  if email and 'password' in request.POST:
    user = authenticate(username=email,password=request.POST['password'])
    if user:
      login(request,user)
      return JsonResponse({'user': {'id': user.id, 'username': user.username, 'email': user.email } })
  if matching_users:
    return JsonResponse({"error": "A user with that email already exists. Please login or use another"},status=400)
  try:
    validate_email(email)
  except forms.ValidationError:
    return JsonResponse({"error": "Please enter a valid email address"},status=400)
  if not ('password' in request.POST and len(request.POST['password']) > 7):
    return JsonResponse({"error": "Please enter a password at least 8 characters long"},status=400)
  username = email.split("@")[0]
  while User.objects.filter(username=username):
    username = email.split("@")[0] + str(random.randint(0000,10000))
  user = User(
    email=email,
    username=username,
  )
  user.set_password(request.POST['password'])
  user.save()
  user.backend='django.contrib.auth.backends.ModelBackend'
  login(request,user)
  return JsonResponse({'user': {'id': user.id, 'username': user.username, 'email': user.email } })
