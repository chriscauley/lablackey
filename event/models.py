from django.db import models
from django.conf import settings
from lablackey.geo.models import Location
import simplejson as json
import datetime

def print_time(t):
  if t: return t.strftime('%I:%M %P')
  return ''

class Schedule(models.Model):
  name = models.CharField(max_length=128,null=True,blank=True)
  date = models.DateField()
  __unicode__ = lambda self: self.name
  class Meta:
    ordering = ("-date",)

class Event(models.Model):
  name = models.CharField(max_length=128,null=True,blank=True)
  date = models.DateField(null=True,blank=True)
  starttime = models.TimeField()
  endtime = models.TimeField(null=True,blank=True)
  location = models.ForeignKey(Location)
  schedule = models.ForeignKey(Schedule,null=True,blank=True)
  description = models.TextField(blank=True)
  def save(self,*args,**kwargs):
    if not self.date and self.schedule:
      self.date = self.schedule.date
    super(Event,self).save(*args,**kwargs)

  @property
  def _json(self):
    return {
      'name': self.name or self.location.name,
      'starttime': print_time(self.starttime),
      'endtime': print_time(self.endtime),
      'lat': self.location.lat,
      'lon': self.location.lon,
      'address': self.location.print_address(),
      'pk': self.id,
      }
  json = property(lambda self: json.dumps(self._json))
  def get_name(self):
    return self.name or self.location

  __unicode__ = lambda self: "%s@%s"%(self.starttime,self.location)
  class Meta:
    ordering = ("-date","starttime")
