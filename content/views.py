from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404

from .models import Page

def page(request,slug):
  if request.user.is_superuser:
    defaults = { 'title': slug.replace('-',' ').title() }
    Page.objects.get_or_create(slug=slug,defaults=defaults)
  values = {
    "page": get_object_or_404(Page, slug=slug),
  }
  return TemplateResponse(request,"content/page.html",values)
