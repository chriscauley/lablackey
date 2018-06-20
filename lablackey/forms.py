from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.db import models
from django import forms
from django.shortcuts import get_object_or_404

from decorators import cached_property

class UserEmailForm(forms.ModelForm):
  class Meta:
    fields = ('email',)
    model = get_user_model()

def NIE(self):
  raise NotImplementedError()

class RequestModelForm(forms.ModelForm):
  """
  Just like a normal form but requires a request as the first argument rather than data.
  Takes GET/POST and FILES from request, so you should NOT pass these in.
  Attaches request to form for later use.

  example_form = RequestModelForm(request,initial={'city':'Houston'})
  user = example_form.request.user
  """
  is_user_form = False
  delete = undelete = NIE
  @property
  def ur_admin(self):
    return reverse(args=[self.__module__.replace(".forms","")])
  def __init__(self,request,*args,**kwargs):
    data = request.POST.copy()
    instance = kwargs.get("instance",None) or self.Meta.model()
    if data and instance:
      # fields that are required can be supplied by the instance if not in data
      # this allows the client to successfully submit a partial form
      for name,field in self.base_fields.items():
        if hasattr(instance,name) and not name in data:
          try:
            data[name] = getattr(instance,name)
          except models.RelatedObjectDoesNotExist:
            pass # thrown when an instance doesn't have a required foreign key
    self.request = request
    super(RequestModelForm,self).__init__(data or None,self.request.FILES or None,*args,**kwargs)
  def save(self,*args,**kwargs):
    commit = kwargs.pop("commit",True)
    kwargs['commit'] = False
    super(RequestModelForm,self).save(*args,**kwargs)
    if self.is_user_form and not self.instance.user:
      self.instance.user = self.request.user
    if commit:
      self.instance.save()
    return self.instance
  @classmethod
  def user_is_allowed(clss,request,method="GET"):
    return request.user.is_authenticated() and request.user.is_superuser
  @classmethod
  def get_list_fields(clss,obj):
    return [
      unicode(obj),
    ]
  @classmethod
  def get_instance(clss,request,id=None):
    if not id:
      return
    return get_object_or_404(clss.Meta.model,id=id)
  def get_queryset(self):
    return self.Meta.model.objects.all()
  @cached_property
  def list_fields(self):
    fields = ['id'] + self.Meta.fields
    fields_map = { f.name: f for f in self.Meta.model._meta.fields }
    def process_field(f):
      if isinstance(fields_map[f],models.ForeignKey):
        return f + "_id"
      return f
    fields = map(process_field,fields)
    return fields

  def obj_to_list(self,obj):
    return [getattr(obj,f) for f in self.list_fields]

  def get_page_json(self,page=1):
    per_page = 100
    page = int(page)
    all_results = self.get_queryset()

    results = all_results
    if page: # zero returns all results
      results = all_results[(page-1)*per_page:page*per_page]
    results = [self.obj_to_list(r) for r in results]

    return dict(
      page=page,
      results=results,
    )

class RequestForm(forms.Form):
  """ Same as above but inherits from Form instead of ModelForm"""
  delete = undelete = NIE
  def __init__(self,request,*args,**kwargs):
    self.request = request
    super(RequestForm,self).__init__(self.request.POST or None,self.request.FILES or None,*args,**kwargs)

class RequestUserModelForm(RequestModelForm):
  """ Users can only ready/write their own data """
  user_field = "user"
  def get_queryset(self,*args,**kwargs):
    qs = super(RequestUserModelForm,self).get_queryset(*args,**kwargs)
    return qs.filter(**{self.user_field: self.request.user})
  @classmethod
  def user_is_allowed(clss,request,method):
    # user is always allowed to modify their own data
    return request.user.is_authenticated()
  @classmethod
  def get_instance(clss,request,id=None):
    if not id:
      return
    if request.user.is_superuser:
      return get_object_or_404(clss.Meta.model,id=id)
    return get_object_or_404(clss.Meta.model,id=id,**{ clss.user_field: request.user })
  def save(self,*args,**kwargs):
    if self.instance.pk:
      if getattr(self.instance,self.user_field) != self.request.user:
        raise NotAllowed()
    else:
      setattr(self.instance,self.user_field,self.request.user)
    return super(RequestUserModelForm,self).save(*args,**kwargs)