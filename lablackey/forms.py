from django.contrib.auth import get_user_model
from django import forms
from django.shortcuts import get_object_or_404

class UserEmailForm(forms.ModelForm):
  class Meta:
    fields = ('email',)
    model = get_user_model()

class RequestModelForm(forms.ModelForm):
  """
  Just like a normal form but requires a request as the first argument rather than data.
  Takes GET/POST and FILES from request, so you should NOT pass these in.
  Attaches request to form for later use.

  example_form = RequestModelForm(request,initial={'city':'Houston'})
  user = example_form.request.user
  """
  is_user_form = False
  def __init__(self,request,*args,**kwargs):
    self.request = request
    super(RequestModelForm,self).__init__(self.request.POST or None,self.request.FILES or None,*args,**kwargs)
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
  def get_instance(self,request,id=None):
    if not id:
      return
    return get_object_or_404(self.Meta.model,id=id)

class RequestForm(forms.Form):
  """ Same as above but inherits from Form instead of ModelForm"""
  def __init__(self,request,*args,**kwargs):
    self.request = request
    super(RequestForm,self).__init__(self.request.POST or None,self.request.FILES or None,*args,**kwargs)
