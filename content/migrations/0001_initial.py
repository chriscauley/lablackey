# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Page'
        db.create_table('content_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('content', ['Page'])

        # Adding model 'Copy'
        db.create_table('content_copy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('context', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.Page'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')(default='change me', max_length=1024)),
        ))
        db.send_create_signal('content', ['Copy'])

        # Adding model 'DesignImage'
        db.create_table('content_designimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['photo.Photo'])),
            ('context', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.Page'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal('content', ['DesignImage'])


    def backwards(self, orm):
        
        # Deleting model 'Page'
        db.delete_table('content_page')

        # Deleting model 'Copy'
        db.delete_table('content_copy')

        # Deleting model 'DesignImage'
        db.delete_table('content_designimage')


    models = {
        'content.copy': {
            'Meta': {'ordering': "('context',)", 'object_name': 'Copy'},
            'body': ('django.db.models.fields.TextField', [], {'default': "'change me'", 'max_length': '1024'}),
            'context': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.Page']", 'null': 'True', 'blank': 'True'})
        },
        'content.designimage': {
            'Meta': {'ordering': "['name']", 'object_name': 'DesignImage'},
            'context': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.Page']", 'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['photo.Photo']"})
        },
        'content.page': {
            'Meta': {'ordering': "['name']", 'object_name': 'Page'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'photo.photo': {
            'Meta': {'object_name': 'Photo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'src': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '300'})
        }
    }

    complete_apps = ['content']
