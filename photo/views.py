from .models import Photo
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse

@login_required
def add_photo(request):
  values = {'photos': Photo.objects.all()}
  return TemplateResponse(request,"photo/add_iframe.html",values)

