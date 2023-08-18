# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-23 05:00
from __future__ import unicode_literals

from django.db import migrations, models
import mycaps.utils


class Migration(migrations.Migration):

    dependencies = [
        ('mycaps', '0002_auto_20180531_0402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coffee',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='description'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coffee',
            name='image',
            field=models.FileField(blank=True, default='', upload_to=mycaps.utils.mycaps_upload_to, verbose_name='image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='color',
            name='background_image',
            field=models.ImageField(blank=True, default='', upload_to=mycaps.utils.mycaps_upload_to, verbose_name='background image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='color',
            name='color',
            field=models.CharField(default='', max_length=200, verbose_name='color'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='color',
            name='color_image',
            field=models.ImageField(blank=True, default='', upload_to=mycaps.utils.mycaps_upload_to, verbose_name='color image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='color',
            name='package_image',
            field=models.ImageField(blank=True, default='', upload_to=mycaps.utils.mycaps_upload_to, verbose_name='package image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='crop',
            name='image',
            field=models.ImageField(blank=True, default='', upload_to=mycaps.utils.mycaps_upload_to, verbose_name='image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='package',
            name='image',
            field=models.ImageField(blank=True, default='', upload_to=mycaps.utils.mycaps_upload_to, verbose_name='image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='package',
            name='image1',
            field=models.ImageField(blank=True, default='', upload_to=mycaps.utils.mycaps_upload_to, verbose_name='image1'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='package',
            name='text1',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='text for capsule'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='package',
            name='text2',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='text for package'),
            preserve_default=False,
        ),
    ]
