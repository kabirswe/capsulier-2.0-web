# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-18 09:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20180601_0441'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['ordering'], 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='category',
            name='ordering',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
