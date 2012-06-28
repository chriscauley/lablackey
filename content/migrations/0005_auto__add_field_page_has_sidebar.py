# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Page.has_sidebar'
        db.add_column('content_page', 'has_sidebar',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Page.has_sidebar'
        db.delete_column('content_page', 'has_sidebar')


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