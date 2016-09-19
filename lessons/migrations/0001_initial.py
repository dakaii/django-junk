# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-19 03:32
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.')], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('facebook_id', models.BigIntegerField(null=True)),
                ('ownerFlg', models.BooleanField(default=False)),
                ('registered_at', models.DateTimeField(auto_now_add=True)),
                ('phoneNumber', models.IntegerField(null=True)),
                ('qro_plan', models.CharField(max_length=50, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('original_id', models.BigIntegerField(blank=True, null=True)),
                ('description', models.CharField(max_length=500)),
                ('registered_by', models.CharField(max_length=100)),
                ('registered_at', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(max_length=100)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateField(blank=True, null=True)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('time_type', models.IntegerField()),
                ('registered_by', models.CharField(max_length=100)),
                ('registered_at', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(max_length=100)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('tutorName', models.CharField(blank=True, max_length=20, null=True)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lessons.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(max_length=100, null=True)),
                ('longitude', models.FloatField(null=True)),
                ('latitude', models.FloatField(null=True)),
                ('original_id', models.CharField(blank=True, max_length=100, null=True)),
                ('direction', models.CharField(blank=True, max_length=300, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=5, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=50, null=True)),
                ('address', models.CharField(max_length=300)),
                ('country_code', models.CharField(blank=True, max_length=5, null=True)),
                ('registered_by', models.CharField(max_length=100)),
                ('updated_by', models.CharField(max_length=100)),
                ('registered_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Password',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_booking', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(max_length=200)),
                ('cuisine_type', models.CharField(max_length=50)),
                ('referUrl', models.URLField(blank=True, null=True)),
                ('tel', models.CharField(blank=True, max_length=12, null=True)),
                ('registered_by', models.CharField(max_length=100)),
                ('updated_by', models.CharField(max_length=100)),
                ('registered_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('shop_location', models.CharField(max_length=100)),
                ('shop_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShopItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=300)),
                ('image_url', models.URLField(blank=True, null=True)),
                ('item_description', models.CharField(max_length=500)),
                ('price', models.CharField(max_length=500)),
                ('category', models.CharField(max_length=500)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop', to='lessons.Shop')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=200)),
                ('dataID', models.CharField(max_length=200)),
                ('registered_by', models.CharField(max_length=100)),
                ('registered_at', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(max_length=100)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.ManyToManyField(related_name='event', to='lessons.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.Location'),
        ),
        migrations.AddField(
            model_name='event',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lessons.Shop'),
        ),
        migrations.AddField(
            model_name='event',
            name='tutorKey',
            field=models.ManyToManyField(blank=True, related_name='tutor', to='lessons.Tutor'),
        ),
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='lessons.Location'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
