# -*- coding: utf-8 -*-
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
            ('has_sidebar', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('content', ['Page'])

        # Adding model 'Copy'
        db.create_table('content_copy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.Page'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('context', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('text', self.gf('django.db.models.fields.CharField')(default='change me', max_length=1024)),
        ))
        db.send_create_signal('content', ['Copy'])

        # Adding model 'DesignImage'
        db.create_table('content_designimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.Page'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('context', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('src', self.gf('sorl.thumbnail.fields.ImageField')(max_length=300, null=True, blank=True)),
        ))
        db.send_create_signal('content', ['DesignImage'])

        # Adding model 'HouseAd'
        db.create_table('content_housead', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.Page'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('src', self.gf('sorl.thumbnail.fields.ImageField')(max_length=300, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('start', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('content', ['HouseAd'])

        # Adding model 'Template'
        db.create_table('content_template', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('content', ['Template'])

        # Adding model 'SideBarWidget'
        db.create_table('content_sidebarwidget', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=99999)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.Page'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.Template'])),
        ))
        db.send_create_signal('content', ['SideBarWidget'])

    def backwards(self, orm):
        # Deleting model 'Page'
        db.delete_table('content_page')

        # Deleting model 'Copy'
        db.delete_table('content_copy')

        # Deleting model 'DesignImage'
        db.delete_table('content_designimage')

        # Deleting model 'HouseAd'
        db.delete_table('content_housead')

        # Deleting model 'Template'
        db.delete_table('content_template')

        # Deleting model 'SideBarWidget'
        db.delete_table('content_sidebarwidget')

    models = {
        'content.copy': {
            'Meta': {'ordering': "('context',)", 'object_name': 'Copy'},
            'context': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.Page']", 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'default': "'change me'", 'max_length': '1024'})
        },
        'content.designimage': {
            'Meta': {'ordering': "['name']", 'object_name': 'DesignImage'},
            'context': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.Page']", 'null': 'True', 'blank': 'True'}),
            'src': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'})
        },
        'content.housead': {
            'Meta': {'ordering': "['name']", 'object_name': 'HouseAd'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.Page']", 'null': 'True', 'blank': 'True'}),
            'src': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'content.page': {
            'Meta': {'ordering': "['name']", 'object_name': 'Page'},
            'has_sidebar': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'content.sidebarwidget': {
            'Meta': {'ordering': "('order',)", 'object_name': 'SideBarWidget'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '99999'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.Page']", 'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.Template']"})
        },
        'content.template': {
            'Meta': {'object_name': 'Template'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['content']