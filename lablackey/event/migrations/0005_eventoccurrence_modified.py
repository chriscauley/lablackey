# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-07-17 21:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_auto_20170712_0413'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventoccurrence',
            name='modified',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2017, 7, 17, 21, 29, 24, 894529)),
            preserve_default=False,
        ),
    ]