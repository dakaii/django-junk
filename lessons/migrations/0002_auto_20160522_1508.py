# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-22 06:08
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='boundingbox',
        ),
        migrations.AddField(
            model_name='location',
            name='bounds',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
    ]
