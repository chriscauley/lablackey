# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Photo.square_crop'
        db.add_column('photo_photo', 'square_crop',
                      self.gf('crop_override.field.CropOverride')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.landscape_crop'
        db.add_column('photo_photo', 'landscape_crop',
                      self.gf('crop_override.field.CropOverride')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Photo.portrait_crop'
        db.add_column('photo_photo', 'portrait_crop',
                      self.gf('crop_override.field.CropOverride')(max_length=100, null=True, blank=True),
                      keep_default=False)


        # Changing field 'Photo.src'
        db.alter_column('photo_photo', 'src', self.gf('crop_override.field.OriginalImage')(max_length=300))
    def backwards(self, orm):
        # Deleting field 'Photo.square_crop'
        db.delete_column('photo_photo', 'square_crop')

        # Deleting field 'Photo.landscape_crop'
        db.delete_column('photo_photo', 'landscape_crop')

        # Deleting field 'Photo.portrait_crop'
        db.delete_column('photo_photo', 'portrait_crop')


        # Changing field 'Photo.src'
        db.alter_column('photo_photo', 'src', self.gf('sorl.thumbnail.fields.ImageField')(max_length=300))
    models = {
        'photo.photo': {
            'Meta': {'object_name': 'Photo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'landscape_crop': ('crop_override.field.CropOverride', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'portrait_crop': ('crop_override.field.CropOverride', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'square_crop': ('crop_override.field.CropOverride', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'src': ('crop_override.field.OriginalImage', [], {'max_length': '300'})
        }
    }

    complete_apps = ['photo']