# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-22 10:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0003_user_facebook_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
