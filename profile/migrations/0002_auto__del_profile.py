# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Profile'
        db.delete_table('profile_profile')


    def backwards(self, orm):
        
        # Adding model 'Profile'
        db.create_table('profile_profile', (
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('profile', ['Profile'])


    models = {
        
    }

    complete_apps = ['profile']
