# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-23 04:56
from __future__ import unicode_literals

from django.db import migrations, models
import page.utils
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conceptmap',
            name='marker',
            field=models.FileField(blank=True, default='', upload_to=page.utils.marker_upload_to),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='partner',
            name='category',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='category'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='partner',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='description'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='partner',
            name='link',
            field=models.URLField(blank=True, default='', verbose_name='link'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='partner',
            name='name',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shop',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254, verbose_name='e-mail'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shop',
            name='logo',
            field=models.FileField(blank=True, default='', upload_to=page.utils.page_upload_to),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shop',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, default='', max_length=128, verbose_name='phone number'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='slider',
            name='button_text',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='button text'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='slider',
            name='title',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='alt tag'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='slider',
            name='url',
            field=models.URLField(blank=True, default='', verbose_name='url'),
            preserve_default=False,
        ),
    ]