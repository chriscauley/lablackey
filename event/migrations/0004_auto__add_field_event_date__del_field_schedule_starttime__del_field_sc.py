# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Event.date'
        db.add_column('event_event', 'date', self.gf('django.db.models.fields.DateField')(null=True, blank=True), keep_default=False)

        # Deleting field 'Schedule.starttime'
        db.delete_column('event_schedule', 'starttime')

        # Deleting field 'Schedule.endtime'
        db.delete_column('event_schedule', 'endtime')

        # Adding field 'Schedule.date'
        db.add_column('event_schedule', 'date', self.gf('django.db.models.fields.DateField')(default=datetime.date(2011, 7, 9)), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Event.date'
        db.delete_column('event_event', 'date')

        # Adding field 'Schedule.starttime'
        db.add_column('event_schedule', 'starttime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)

        # Adding field 'Schedule.endtime'
        db.add_column('event_schedule', 'endtime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)

        # Deleting field 'Schedule.date'
        db.delete_column('event_schedule', 'date')


    models = {
        'event.event': {
            'Meta': {'ordering': "('-date', 'starttime')", 'object_name': 'Event'},
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'endtime': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['event.Schedule']", 'null': 'True', 'blank': 'True'}),
            'starttime': ('django.db.models.fields.TimeField', [], {})
        },
        'event.schedule': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Schedule'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'geo.city': {
            'Meta': {'object_name': 'City'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latlon': ('lablackey.geo.widgets.LocationField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2'})
        },
        'geo.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['geo.City']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latlon': ('lablackey.geo.widgets.LocationField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.IntegerField', [], {'default': '77007'})
        }
    }

    complete_apps = ['event']
