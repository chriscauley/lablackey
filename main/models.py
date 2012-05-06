from django.db import models
from articles.models import Article

class OrderedModel(models.Model):
  order = models.PositiveIntegerField(default=9999)
  class Meta:
    abstract = True

class SlugModel(models.Model):
  title = models.CharField(max_length=128)
  __unicode__ = lambda self: self.title
  slug = models.CharField(max_length=128,null=True,blank=True)

  def save (self,*args,**kwargs):
    self.slug = slugify(self.title)
    super(SlugModel,self).save(*args,**kwargs)

  class Meta:
    abstract = True
