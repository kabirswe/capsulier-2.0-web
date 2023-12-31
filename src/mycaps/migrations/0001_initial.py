# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-31 02:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mycaps.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coffee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('image', models.FileField(blank=True, null=True, upload_to=mycaps.utils.mycaps_upload_to, verbose_name='image')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, null=True, verbose_name='updated on')),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='name')),
                ('color', models.CharField(max_length=200, null=True, verbose_name='color')),
                ('image', models.ImageField(upload_to=mycaps.utils.mycaps_upload_to, verbose_name='image')),
                ('color_image', models.ImageField(blank=True, null=True, upload_to=mycaps.utils.mycaps_upload_to, verbose_name='color image')),
                ('package_image', models.ImageField(blank=True, null=True, upload_to=mycaps.utils.mycaps_upload_to, verbose_name='package image')),
                ('background_image', models.ImageField(blank=True, null=True, upload_to=mycaps.utils.mycaps_upload_to, verbose_name='background image')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, null=True, verbose_name='updated on')),
            ],
        ),
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=mycaps.utils.mycaps_upload_to, verbose_name='image')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, null=True, verbose_name='updated on')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'crop',
                'verbose_name_plural': 'cropes',
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=mycaps.utils.mycaps_upload_to, verbose_name='image')),
                ('image1', models.ImageField(blank=True, null=True, upload_to=mycaps.utils.mycaps_upload_to, verbose_name='image1')),
                ('text1', models.CharField(blank=True, max_length=200, null=True, verbose_name='text for capsule')),
                ('text2', models.CharField(blank=True, max_length=200, null=True, verbose_name='text for package')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, null=True, verbose_name='updated on')),
                ('coffee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='packagebycoffee', to='mycaps.Coffee', verbose_name='coffee')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='packagebycolor', to='mycaps.Color', verbose_name='color')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'package',
                'verbose_name_plural': 'packages',
            },
        ),
    ]
