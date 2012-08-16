from django.db import models
from django.template.defaultfilters import striptags
from PIL import Image
from sorl.thumbnail import ImageField
from lablackey.db.models import OrderedModel

context_help = "Refers to the location on the website. Please do not change."
body_help = "Shift+enter adds a line-break, enter starts a new paragraph."

class Page(models.Model):
  name = models.CharField(max_length=32)
  has_sidebar = models.BooleanField(default=False)

  class Meta:
    ordering = ['name']

  __unicode__ = lambda self: self.name

class PageItemModel(models.Model):
  page = models.ForeignKey(Page,null=True,blank=True)
  name = models.CharField(max_length=256,null=True,blank=True)
  __unicode__ = lambda self: "%s: %s"%(self.page,self.name)
  class Meta:
    abstract = True

class PageContentModel(PageItemModel):
  context = models.CharField(max_length=32,help_text=context_help)
  def save(self,*args,**kwargs):
    if not self.page:
      self.page = Page.objects.get_or_create(name = self.context.split('-')[0])[0]
    if not self.name:
      self.name = ' '.join(self.context.split('-')[1:])
    super(PageContentModel,self).save(*args,**kwargs)
  class Meta:
    abstract = True

class Copy(PageContentModel):
  text = models.CharField(max_length=1024,help_text=body_help,default="change me")
  class Meta:
    verbose_name_plural = "Copy"
    ordering = ("context",)

class DesignImage(PageContentModel):
  src = ImageField("Image",upload_to='uploads/photos/%Y-%m',max_length=300,null=True,blank=True)
  class Meta:
    ordering = ['name']

class HouseAd(PageItemModel):
  src = ImageField("Image",upload_to='uploads/photos/%Y-%m',max_length=300,null=True,blank=True)
  url = models.URLField(null=True,blank=True)
  active = models.BooleanField(default=False)
  start = models.DateField(null=True,blank=True)
  end = models.DateField(null=True,blank=True)
  class Meta:
    ordering = ['name']

class Template(models.Model):
  template = models.CharField(max_length=64)
  name = models.CharField(max_length=64)
  __unicode__ = lambda self: self.name

class SideBarWidget(PageItemModel,OrderedModel):
  template = models.ForeignKey(Template)
  class Meta:
    ordering = ('order',)
