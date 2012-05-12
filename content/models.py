from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import striptags, truncatewords
from PIL import Image
from lablackey.db.models import SlugModel, OrderedModel
from lablackey.photo.models import Photo
#import sorl.thumbnail
from django.conf import settings
from django.core.files import File

context_help = "Refers to the location on the website. Please do not change."
body_help = "Shift+enter adds a line-break, enter starts a new paragraph."

class Page(SlugModel):
  pass

class PageContentModel(models.Model):
  context = models.CharField(max_length=32,help_text=context_help)
  page = models.ForeignKey(Page,null=True,blank=True)
  name = models.CharField(max_length=256,null=True,blank=True)
  def save(self,*args,**kwargs):
    if not self.page:
      self.page = Page.objects.get_or_create(title = self.context.split('-')[0])[0]
    if not self.name:
      self.name = ' '.join(self.context.split('-')[1:])
    super(PageContentModel,self).save(*args,**kwargs)
  class Meta:
    abstract = True
  __unicode__ = lambda self: "%s: %s"%(self.page,self.name)

class Copy(PageContentModel):
  body = models.TextField(max_length=1024,help_text=body_help,default="change me")
  text = lambda self: striptags(self.body)[:200]
  class Meta:
    verbose_name_plural = "Copy"
    ordering = ("id",)

class DesignImage(PageContentModel):
  class Meta:
    ordering = ['name']
    verbose_name_plural = 'Images'
  credit = models.CharField(max_length=32,null=True,blank=True)
  credit_url = models.URLField(verify_exists=False,null=True,blank=True)
  alt_text = models.CharField("Hover Text",max_length=128,null=True,blank=True)
  src  = models.ImageField(
    'Image', max_length=300,
    upload_to = settings.UPLOAD_DIR + '/designphotos/',
    null=True,blank=True)

class Section(OrderedModel,SlugModel):
  hide_title = models.BooleanField(default=False)
  page = models.ForeignKey(Page)
  body = models.TextField()
  adh = "Update description every time the body is changed."
  auto_description = models.BooleanField("Auto-update Description",default=False,help_text=adh)
  dh = "For the front page, will be automatically generated if blank."
  description = models.TextField(null=True,blank=True,help_text=dh)
  def save(self,*args,**kwargs):
    if self.auto_description or not self.description:
      self.description = truncatewords(striptags(self.body),30)
    super(Section,self).save(*args,**kwargs)
  class Meta:
    ordering = ("order",)

class PageImage(OrderedModel):
  page = models.ForeignKey(Page)
  photo = models.ForeignKey(Photo)
  caption_override = models.CharField(max_length=512,null=True,blank=True)
  caption = lambda self: self.caption_override or self.photo.caption
  def edit(self):
    if self.photo:
      return "<a href='/admin/photo/photo/%s' target='_blank'>edit photo</a>"%self.photo.id
    return ''
  edit.allow_tags = True
  class Meta:
    ordering = ("order",)
