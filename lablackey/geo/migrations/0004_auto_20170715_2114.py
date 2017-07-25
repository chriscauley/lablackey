# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-07-15 21:14
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0003_location_extra'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2017, 7, 15, 21, 14, 41, 546515)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='city',
            name='modified',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2017, 7, 15, 21, 14, 46, 541380)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2017, 7, 15, 21, 14, 54, 575320)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='modified',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2017, 7, 15, 21, 14, 56, 593281)),
            preserve_default=False,
        ),
    ]