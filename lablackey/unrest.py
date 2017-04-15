# This file should eventually become it's own unrest library, but then again all of lablackey might go that way

from django.db import models
from django import forms

EXCLUDE_FIELDS = ['django.db.models.AutoField']

FIELD_MAP = {
  'django.db.models.CharField': { },
  'django_countries.fields.CountryField': { },
}

def form_to_schema(form):
  schema = []
  initial = {}
  instance = form.instance
  for name,field in form.fields.items():
    json = field.widget.attrs
    json.update({
      'required': field.required,
      'name': name,
      'label': field.label,
      'help_text': field.help_text
    })
    if form.instance:
      initial[name] = field.initial or getattr(form.instance,name)
    if not json['help_text']:
      json['help_text'] = form.Meta.model._meta.get_field(name).help_text
    if hasattr(field,'choices'):
      json['choices'] = field.choices
    if isinstance(field.widget,forms.widgets.RadioSelect):
      json['type'] = 'radio'
    schema.append(json)
  return {
    'schema': schema,
    'initial': initial,
    'errors':   { k: e.get_json_data()[0]['message'] for k,e in form.errors.items() } or None,
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
