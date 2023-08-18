# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-31 02:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import geoposition.fields
import image_cropping.fields
import page.utils
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConceptMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', geoposition.fields.GeopositionField(max_length=42, verbose_name='address')),
                ('marker', models.FileField(blank=True, null=True, upload_to=page.utils.marker_upload_to)),
                ('name', models.CharField(blank=True, max_length=200, unique=True, verbose_name='name')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, null=True, verbose_name='updated on')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='updated by')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'concept map',
                'verbose_name_plural': 'concept maps',
            },
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, verbose_name='content')),
                ('content_fr', models.TextField(blank=True, null=True, verbose_name='content')),
                ('content_en', models.TextField(blank=True, null=True, verbose_name='content')),
                ('content_es', models.TextField(blank=True, null=True, verbose_name='content')),
                ('ordering', models.PositiveIntegerField(default=0)),
                ('title', models.CharField(max_length=120, verbose_name='title')),
                ('title_fr', models.CharField(max_length=120, null=True, verbose_name='title')),
                ('title_en', models.CharField(max_length=120, null=True, verbose_name='title')),
                ('title_es', models.CharField(max_length=120, null=True, verbose_name='title')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, null=True, verbose_name='updated on')),
            ],
            options={
                'ordering': ['ordering'],
                'verbose_name': 'faq',
                'verbose_name_plural': 'faq',
            },
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('category', models.CharField(blank=True, max_length=200, null=True, verbose_name='category')),
                ('category_fr', models.CharField(blank=True, max_length=200, null=True, verbose_name='category')),
                ('category_en', models.CharField(blank=True, max_length=200, null=True, verbose_name='category')),
                ('category_es', models.CharField(blank=True, max_length=200, null=True, verbose_name='category')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('description_fr', models.TextField(blank=True, null=True, verbose_name='description')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='description')),
                ('description_es', models.TextField(blank=True, null=True, verbose_name='description')),
                ('index', models.PositiveIntegerField(default=0)),
                ('image', models.ImageField(upload_to=page.utils.page_upload_to, verbose_name='image')),
                ('image_cropping', image_cropping.fields.ImageRatioField(b'image', '0x0', adapt_rotation=False, allow_fullsize=False, free_crop=True, help_text=None, hide_image_field=False, size_warning=False, verbose_name='image cropping')),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='name')),
                ('name_fr', models.CharField(blank=True, max_length=200, null=True, verbose_name='name')),
                ('name_en', models.CharField(blank=True, max_length=200, null=True, verbose_name='name')),
                ('name_es', models.CharField(blank=True, max_length=200, null=True, verbose_name='name')),
                ('slug', models.SlugField(editable=False, verbose_name='slug')),
                ('link', models.URLField(blank=True, null=True, verbose_name='link')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, null=True, verbose_name='updated on')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('sites', models.ManyToManyField(to='sites.Site', verbose_name='sites')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='updated by')),
            ],
            options={
                'ordering': ['index'],
                'verbose_name': 'Partner',
                'verbose_name_plural': 'Partners',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('afternoon_end_time', models.TimeField(blank=True, null=True, verbose_name='afternoon end time')),
                ('afternoon_start_time', models.TimeField(blank=True, null=True, verbose_name='afternoon start time')),
                ('close', models.BooleanField(default=False, verbose_name='close')),
                ('day', models.CharField(choices=[(b'1', 'Monday'), (b'2', 'Tuesday'), (b'3', 'Wednesday'), (b'4', 'Thursday'), (b'5', 'Friday'), (b'6', 'Saturday'), (b'7', 'Sunday')], max_length=2, verbose_name='day')),
                ('morning_end_time', models.TimeField(blank=True, null=True, verbose_name='morning end time')),
                ('morning_start_time', models.TimeField(blank=True, null=True, verbose_name='morning start time')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, null=True, verbose_name='updated on')),
            ],
            options={
                'verbose_name': 'schedule',
                'verbose_name_plural': 'schedules',
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('address', geoposition.fields.GeopositionField(max_length=42, verbose_name='address')),
                ('address2', models.CharField(blank=True, max_length=180, verbose_name='address2')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='e-mail')),
                ('image', models.ImageField(help_text='At least 800px wide', upload_to=page.utils.page_upload_to, verbose_name='image')),
                ('image_cropping', image_cropping.fields.ImageRatioField(b'image', '0x0', adapt_rotation=False, allow_fullsize=False, free_crop=True, help_text=None, hide_image_field=False, size_warning=False, verbose_name='image cropping')),
                ('logo', models.FileField(blank=True, null=True, upload_to=page.utils.page_upload_to)),
                ('name', models.CharField(blank=True, max_length=200, unique=True, verbose_name='name')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, verbose_name='phone number')),
                ('slug', models.SlugField(editable=False, unique=True, verbose_name='slug')),
                ('website', models.URLField(blank=True, verbose_name='website')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, null=True, verbose_name='updated on')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('sites', models.ManyToManyField(to='sites.Site', verbose_name='sites')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='updated by')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'shop',
                'verbose_name_plural': 'shops',
            },
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('button_text', models.CharField(blank=True, max_length=200, null=True, verbose_name='button text')),
                ('button_text_fr', models.CharField(blank=True, max_length=200, null=True, verbose_name='button text')),
                ('button_text_en', models.CharField(blank=True, max_length=200, null=True, verbose_name='button text')),
                ('button_text_es', models.CharField(blank=True, max_length=200, null=True, verbose_name='button text')),
                ('index', models.PositiveIntegerField(default=0)),
                ('image', models.ImageField(upload_to=page.utils.page_upload_to, verbose_name='image')),
                ('image_cropping', image_cropping.fields.ImageRatioField(b'image', '1600x1067', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='image cropping')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='alt tag')),
                ('title_fr', models.CharField(blank=True, max_length=200, null=True, verbose_name='alt tag')),
                ('title_en', models.CharField(blank=True, max_length=200, null=True, verbose_name='alt tag')),
                ('title_es', models.CharField(blank=True, max_length=200, null=True, verbose_name='alt tag')),
                ('slug', models.SlugField(blank=True, null=True, verbose_name='slug')),
                ('url', models.URLField(blank=True, null=True, verbose_name='url')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, null=True, verbose_name='updated on')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('sites', models.ManyToManyField(to='sites.Site', verbose_name='sites')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='updated by')),
            ],
            options={
                'ordering': ['-index'],
                'verbose_name': 'Slider',
                'verbose_name_plural': 'Slider',
            },
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200, verbose_name='first name')),
                ('image', models.ImageField(upload_to=page.utils.page_upload_to, verbose_name='image')),
                ('image_cropping', image_cropping.fields.ImageRatioField(b'image', '1200x1800', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='image cropping')),
                ('last_name', models.CharField(max_length=200, verbose_name='last name')),
                ('slug', models.SlugField(editable=False, verbose_name='slug')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, null=True, verbose_name='updated on')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page.Shop', verbose_name='shop')),
            ],
            options={
                'verbose_name': 'team member',
                'verbose_name_plural': 'team members',
            },
        ),
        migrations.AddField(
            model_name='schedule',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page.Shop', verbose_name='shop'),
        ),
        migrations.AlterUniqueTogether(
            name='schedule',
            unique_together=set([('shop', 'day')]),
        ),
    ]