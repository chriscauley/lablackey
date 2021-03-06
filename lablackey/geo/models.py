from django.db import models
from django.conf import settings
from localflavor.us.models import USStateField

from .widgets import LocationField
from lablackey.decorators import cached_property
from lablackey.db.models import JsonModel

from jsonfield import JSONField
import json
import urllib

try:
  import ezdxf
except ImportError:
  ezdxf = None

class GeoModel(JsonModel):
  latlon = LocationField(max_length=500,null=True,blank=True) # stored as lat,lon
  _lat = property(lambda self: float(self.latlon.split(",")[0]))
  _lon = property(lambda self: float(self.latlon.split(",")[1]))
  @property
  def lat(self):
    if self.latlon: return self._lat
    return False
  @property
  def lon(self):
    if self.latlon: return self._lon
    return False
  class Meta:
    abstract = True

class City(GeoModel):
  name = models.CharField(max_length=128)
  state = USStateField()
  def __unicode__(self):
    return "%s, %s"%(self.name,self.state)
  class Meta:
    ordering = ('name',)
    verbose_name_plural = "Cities"

class Location(GeoModel):
  name = models.CharField(max_length=128,null=True,blank=True)
  parent = models.ForeignKey("self",null=True,blank=True)
  _ht = "Optional. Alternative name for the calendar."
  short_name = models.CharField(max_length=64,null=True,blank=True,help_text=_ht)
  get_short_name = lambda self: self.short_name or self.name
  _short_name = property(get_short_name)
  address = models.CharField(max_length=64,null=True,blank=True)
  address2 = models.CharField(max_length=64,null=True,blank=True)
  city = models.ForeignKey(City,default=1)
  zip_code = models.IntegerField(default=77007)
  extra = JSONField(default=dict,blank=True)
  dxf = models.FileField(upload_to="floorplans",null=True,blank=True)
  __unicode__ = lambda self: self.name
  city_name = property(lambda self: self.city.name)
  state = property(lambda self: self.city.state)
  def save(self,*args,**kwargs):
    super(Location,self).save(*args,**kwargs)
    if self.dxf:
      self.generate_dxf_entities()
  json_fields = ['id','name','lat','lon','address','address2','city_name','zip_code','state','_short_name']
  def generate_dxf_entities(self):
    if not ezdxf:
      return
    dwg = ezdxf.readfile(self.dxf.path)
    modelspace = dwg.modelspace()
    for e in modelspace:
      if e.dxftype() == "LWPOLYLINE":
        geometry = [list(i)[:2] for i in e.get_points()]
      elif e.dxftype() == "LINE":
        geometry = [e.dxf.start,e.dxf.end]
      else:
        continue
      dxf,new = DXFEntity.objects.get_or_create(
        dxftype = e.dxftype(),
        points = json.dumps([[round(i) for i in p] for p in geometry])
      )
      if new:
        print("New DXFEntity: %s"%dxf)
        
  class Meta:
    ordering = ('name',)

  def print_address(self):
    l = [self.name,self.address,self.address2,self.city.__unicode__(),self.zip_code]
    return '\n'.join([str(li) for li in l if li])

class RoomGroup(models.Model):
  name = models.CharField(max_length=16)
  color = models.CharField(max_length=32)
  fill = models.ForeignKey('media.Photo',null=True,blank=True)
  __unicode__ = lambda self: self.name
  @property
  def as_json(self):
    return {
      'name': self.name,
      'color': self.color,
      'fill': self.fill.file.url if self.fill else None,
    }

class Room(models.Model):
  name = models.CharField(max_length=128,null=True,blank=True)
  location = models.ForeignKey(Location)
  _ht = "Optional. Alternative name for the calendar."
  short_name = models.CharField(max_length=64,null=True,blank=True,help_text=_ht)
  get_short_name = lambda self: self.short_name or self.name
  in_calendar = models.BooleanField("can be scheduled for events",default=True)
  has_checkoutitems = models.BooleanField(default=False)
  roomgroup = models.ForeignKey(RoomGroup,null=True,blank=True)
  map_key = models.CharField(max_length=1,null=True,blank=True)
  def get_map_link(self):
    location = self.location
    lines = [location.name,location.address,location.city.name,location.city.state]
    return "http://maps.google.com/?q="+urllib.quote(", ".join([unicode(l) for l in lines if l]))
  @property
  def as_json(self):
    return {
      'id': self.id,
      'name': self.name,
      'roomgroup_id': self.roomgroup_id,
      'short_name': self.get_short_name(),
      'in_calendar': self.in_calendar,
      'map_key': self.map_key,
      'map_link': self.get_map_link(),
    }
  __unicode__ = lambda self: "%s"%(self.name or self.location)
  class Meta:
    ordering = ('name',)
    unique_together = ('name','location')

class DXFEntity(models.Model):
  points = models.TextField()
  dxftype = models.CharField(max_length=16)
  room = models.ForeignKey(Room,null=True,blank=True)
  __unicode__ = lambda self: "%s #%s (%s)"%(self.dxftype,self.id,self.room)
  @property
  def as_json(self):
    return {
      'id': self.pk,
      'points': json.loads(self.points),
      'dxftype': self.dxftype,
      'room_id': self.room_id
    }
  class Meta:
    ordering = ('pk',)
