from django.db import models
from django.contrib.auth.models import User

class ProfileManager(models.Manager):
  def from_user(user):
    user = getattr(user,"user",False) or user
    profile,new = self.get_or_create(user=user)
    return profile

class ProfileModel(models.Model):
  user = models.OneToOneField(User)
  ghandle = models.CharField(max_length=256,null=True,blank=True)
  objects = ProfileManager()
  __unicode__ = lambda self: "%s's Profile"%self.user
  class Meta:
    abstract = True

class UserModel(models.Model):
  user = models.ForeignKey(User)
  class Meta:
    abstract = True
