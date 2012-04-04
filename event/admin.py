from django.contrib import admin
from lablackey.event.models import Event, Schedule

class EventInline(admin.TabularInline):
  model = Event
  fields = ('name','starttime','endtime','location')

class ScheduleAdmin(admin.ModelAdmin):
  inlines = (EventInline,)

class EventAdmin(admin.ModelAdmin):
  list_display = ("__unicode__","schedule",)
  list_filter = ("schedule",)

admin.site.register(Event,EventAdmin)
admin.site.register(Schedule,ScheduleAdmin)
