# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Copy.body'
        db.delete_column('content_copy', 'body')

        # Adding field 'Copy.text'
        db.add_column('content_copy', 'text',
                      self.gf('django.db.models.fields.CharField')(default='change me', max_length=1024),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Copy.body'
        db.add_column('content_copy', 'body',
                      self.gf('django.db.models.fields.TextField')(default='change me', max_length=1024),
                      keep_default=False)

        # Deleting field 'Copy.text'
        db.delete_column('content_copy', 'text')


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
        'content.page': {
            'Meta': {'ordering': "['name']", 'object_name': 'Page'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['content']