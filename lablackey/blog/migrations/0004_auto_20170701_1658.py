# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-07-01 16:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20170416_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_type',
            field=models.CharField(choices=[[b'blog', b'blog'], [b'flatpage', b'flatpage']], default=[b'blog', b'blog'], max_length=64),
        ),
        migrations.AddField(
            model_name='post',
            name='template',
            field=models.CharField(choices=[(b'default', b'default')], default=(b'default', b'default'), max_length=64),
        ),
    ]
