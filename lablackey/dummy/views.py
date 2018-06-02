from django.conf import settings
from django.contrib.auth import get_user_model
from django.http.response import HttpResponse

def reset(request):
  reset_email = request.GET.get('reset_email',"")
  User = get_user_model()
  for email,password in settings.DUMMY_USERS:
    if reset_email and reset_email != email: # will reset all if ?reset_email is none
      continue
    try:
      user = User.objects.get(email=email)
    except User.DoesNotExist:
      user = User.objects.create_user(email,email=email,password=password)
      # count how many users were created ?
    for related_name in settings.DUMMY_RELATED_NAMES:
      getattr(user,related_name).all().delete()
      # count how many items were deleted?
  return HttpResponse("Ok")