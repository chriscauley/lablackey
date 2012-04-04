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
            ('context', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.Page'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('credit', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('credit_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('alt_text', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('src', self.gf('django.db.models.fields.files.ImageField')(max_length=300, null=True, blank=True)),
        ))
        db.send_create_signal('content', ['DesignImage'])

        # Adding model 'ItemList'
        db.create_table('content_itemlist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('context', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.Page'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('columns', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('show_logo', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('show_url', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('show_description', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('show_order', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('show_last_name', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('content', ['ItemList'])

        # Adding model 'ListItem'
        db.create_table('content_listitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('itemlist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.ItemList'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=200, null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('content', ['ListItem'])


    def backwards(self, orm):
        
        # Deleting model 'Page'
        db.delete_table('content_page')

        # Deleting model 'Copy'
        db.delete_table('content_copy')

        # Deleting model 'DesignImage'
        db.delete_table('content_designimage')

        # Deleting model 'ItemList'
        db.delete_table('content_itemlist')

        # Deleting model 'ListItem'
        db.delete_table('content_listitem')


    models = {
        'content.copy': {
            'Meta': {'ordering': "('id',)", 'object_name': 'Copy'},
            'body': ('django.db.models.fields.TextField', [], {'default': "'change me'", 'max_length': '1024'}),
            'context': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.Page']", 'null': 'True', 'blank': 'True'})
        },
        'content.designimage': {
            'Meta': {'ordering': "['name']", 'object_name': 'DesignImage'},
            'alt_text': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'context': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'credit': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'credit_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.Page']", 'null': 'True', 'blank': 'True'}),
            'src': ('django.db.models.fields.files.ImageField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'})
        },
        'content.itemlist': {
            'Meta': {'object_name': 'ItemList'},
            'columns': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'context': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.Page']", 'null': 'True', 'blank': 'True'}),
            'show_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_last_name': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_logo': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_order': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_url': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'content.listitem': {
            'Meta': {'ordering': "('last_name', 'order', 'name')", 'object_name': 'ListItem'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'itemlist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.ItemList']"}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'content.page': {
            'Meta': {'object_name': 'Page'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['content']
