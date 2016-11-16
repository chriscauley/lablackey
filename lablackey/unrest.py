
# This file should eventually become it's own unrest library, but then again all of lablackey might go that way

EXCLUDE_FIELDS = ['django.db.models.AutoField']

FIELD_MAP = {
  'django.db.models.CharField': { },
  'django_countries.fields.CountryField': { },
}

def model_to_schema(model):
  schema = []
  exclude = getattr(model,"schema_exclude",[])
  for field, fk_model in model._meta.get_fields_with_model():
    name, path, args, kwargs = field.deconstruct()
    if path in EXCLUDE_FIELDS or name in exclude:
      continue
    json = FIELD_MAP.get(path,{}).copy()
    json['name'] = name
    if kwargs.get('null',False) or kwargs.get('blank',False):
      json['required'] = False
    schema.append(json)
  return schema
    
  
