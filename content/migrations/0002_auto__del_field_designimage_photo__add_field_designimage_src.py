# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'DesignImage.photo'
        db.delete_column('content_designimage', 'photo_id')

        # Adding field 'DesignImage.src'
        db.add_column('content_designimage', 'src', self.gf('sorl.thumbnail.fields.ImageField')(max_length=300, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'DesignImage.photo'
        raise RuntimeError("Cannot reverse this migration. 'DesignImage.photo' and its values cannot be restored.")

        # Deleting field 'DesignImage.src'
        db.delete_column('content_designimage', 'src')


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
            'src': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'})
        },
        'content.page': {
            'Meta': {'ordering': "['name']", 'object_name': 'Page'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['content']
