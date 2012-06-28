# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Photo'
        db.create_table('photo_photo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('src', self.gf('sorl.thumbnail.fields.ImageField')(max_length=300)),
        ))
        db.send_create_signal('photo', ['Photo'])


    def backwards(self, orm):
        # Deleting model 'Photo'
        db.delete_table('photo_photo')


    models = {
        'photo.photo': {
            'Meta': {'object_name': 'Photo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'src': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '300'})
        }
    }

    complete_apps = ['photo']