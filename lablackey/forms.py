from django.contrib.auth import get_user_model
from django import forms

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
  def __init__(self,request,*args,**kwargs):
    data = request.POST or request.GET or None
    files = request.FILES or None
    super(RequestModelForm,self).__init__(data,files,*args,**kwargs)
    self.request = request
