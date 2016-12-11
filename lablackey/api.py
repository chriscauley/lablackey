from django.apps import apps
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.core import serializers

def get_model(app_name,model_name):
  return apps.get_app_config(app_name).get_model(model_name)

def serialize(obj):
  return {f: getattr(obj,f) for f in obj.json_fields}

def get_one(request,app_name,model_name,pk):
  model = get_model(app_name,model_name)
  obj = get_object_or_404(model,pk=pk)
  return JsonResponse({'data': serialize(obj)})

def get_many(request,app_name,model_name):
  model = get_model(app_name,model_name)
  objs = model.objects.all()
  return JsonResponse({'data': [serialize(o) for o in objs]})
