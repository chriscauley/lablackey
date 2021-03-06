# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-02-23 16:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from lablackey.sms import models as sms_models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SMSNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=16, unique=True)),
                ('verified', models.DateTimeField(blank=True, null=True)),
                ('code', models.IntegerField(default=sms_models.random_code)),
                ('expire', models.DateTimeField(default=sms_models.expiry)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
