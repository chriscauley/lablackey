from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import striptags
from PIL import Image
#import sorl.thumbnail
from django.conf import settings
from django.core.files import File

context_help = "Refers to the location on the website. Please do not change."
body_help = "Shift+enter adds a line-break, enter starts a new paragraph."

class Page(models.Model):
    name = models.CharField(max_length=32)
    def __unicode__(self):
        return self.name

class PageContentModel(models.Model):
    context = models.CharField(max_length=32,help_text=context_help)
    page = models.ForeignKey(Page,null=True,blank=True)
    name = models.CharField(max_length=256,null=True,blank=True)
    def save(self,*args,**kwargs):
        if not self.page:
            self.page = Page.objects.get_or_create(name = self.context.split('-')[0])[0]
        if not self.name:
            self.name = ' '.join(self.context.split('-')[1:])
        super(PageContentModel,self).save(*args,**kwargs)
    class Meta:
        abstract = True
    def __unicode__(self):
        return "%s: %s"%(self.page,self.name)

class Copy(PageContentModel):
    body = models.TextField(max_length=1024,help_text=body_help,default="change me")
    def text(self):
        return striptags(self.body)[:200]
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
        'Image', max_length=300, #help_text = help_text,
        upload_to = settings.UPLOAD_DIR + '/designphotos/',
        null=True,blank=True)

    def copyright_div(self):
        c = self.credit
        if self.credit_url:
            c = '<a href="%s">%s</a>'%(self.credit_url,self.credit)
        if c: 
            return "<div class='copyright'>&copy; %s</div>"%c
        else: return ''

class ItemList(PageContentModel):
    class Meta:
        verbose_name_plural = "Lists"
    columns = models.IntegerField(default=1)

    show_logo = models.BooleanField(default=True)
    show_url = models.BooleanField(default=True)
    show_description = models.BooleanField(default=True)
    show_order = models.BooleanField(default=True)
    show_last_name = models.BooleanField(default=True)

    @property
    def column_percent(self):
        return 100/self.column_number
    @property
    def column_number(self):
        return min(self.columns,self.listitem_set.count() or 1)
    @property
    def columnized_items(self):
        from itertools import cycle
        import math
        c = self.columns
        l = list(self.listitem_set.all())
        r = int(math.ceil(float(len(l))/c))
        n = len(l)
        bins = []; s = 0; ic = c*1
        while True:
            e = int(math.ceil(float(n-s)/ic))+s
            bins.append(l[s:e])
            s = e
            ic -= 1
            if s >= n:
                break
        c = cycle(bins)
        out = []
        for i in range(n):
            out.append(c.next().pop(0))
        return out

class ListItem(models.Model):
    itemlist = models.ForeignKey(ItemList)
    name = models.CharField(max_length=128)
    last_name = models.CharField("Last Name",max_length=64,null=True,blank=True)
    logo = models.ImageField(max_length=200,upload_to=settings.UPLOAD_DIR + '/logos/%Y-%m',
                             null=True,blank=True)
    order = models.IntegerField(default=0)
    url = models.URLField(verify_exists=False,max_length=200,null=True,blank=True)
    description = models.TextField(null=True,blank=True)

    class Meta:
        ordering = ('last_name','order','name')
