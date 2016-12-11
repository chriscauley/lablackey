# This file should eventually become it's own unrest library, but then again all of lablackey might go that way

from django.db import models

EXCLUDE_FIELDS = ['django.db.models.AutoField']

FIELD_MAP = {
  'django.db.models.CharField': { },
  'django_countries.fields.CountryField': { },
}

def model_to_schema(model):
  schema = []
  exclude = getattr(model,"schema_exclude",[])
  for field in model._meta.get_fields():
    if isinstance(field,models.ManyToOneRel):
      continue
    name, path, args, kwargs = field.deconstruct()
    if path in EXCLUDE_FIELDS or name in exclude:
      continue
    json = FIELD_MAP.get(path,{}).copy()
    json['name'] = name
    if kwargs.get('null',False) or kwargs.get('blank',False):
      json['required'] = False
    if kwargs.get("choices",None):
      json['type'] = 'select'
      json['choice_tuples'] = kwargs['choices']
    schema.append(json)
  return schema
    
  
