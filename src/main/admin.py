""" Admin for the main app """

import django.db.models

from django.contrib import admin
from django.contrib.admin.models import LogEntry, DELETION
from django.core.urlresolvers import reverse
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from adminsortable2.admin import SortableAdminMixin
from easy_select2.widgets import Select2, Select2Multiple
from image_cropping import ImageCroppingMixin
from import_export.admin import ImportExportActionModelAdmin
from modeltranslation.admin import TranslationAdmin

from . import models
from . import widgets

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Admins
@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):

    # date_hierarchy = 'action_time'

    readonly_fields = ('get_readonly_fields', )

    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
        'change_message',
    ]

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.get_fields()]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = u'<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return link
    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'object'

    def queryset(self, request):
        return super(LogEntryAdmin, self).queryset(request) \
            .prefetch_related('content_type')


@admin.register(models.Page)
class PageAdmin(ImportExportActionModelAdmin, TranslationAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'html',
            )
        }),
        (_('Meta data'), {
            'classes': ('collapse',),
            'fields': (
                'id',
                'slug',
                'created_on',
                'updated_on',
            ),
        }),
    )
    list_display = (
        'name_fr',
        'name_en',
        'html',
        'text_count',
        'updated_on',
    )
    list_display_links = (
        'name_fr',
        'name_en',
    )
    readonly_fields = (
        'id',
        'slug',
        'created_on',
        'updated_on',
    )


@admin.register(models.SEO)
class SEOAdmin(ImageCroppingMixin, TranslationAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'page',
            )
        }),
        (_('Meta'), {
            'fields': (
                'title',
                'description',
                'keywords',
                'resource_type',
                'image',
                'image_cropping',
            )
        }),
        (_('Facebook'), {
            'fields': (
                'fb_app_id',
                'site_name',
            )
        }),
        (_('Twitter'), {
            'fields': (
                'twitter_site',
            )
        }),
        (_('Meta data'), {
            'classes': ('collapse',),
            'fields': (
                'id',
                'created_on',
                'updated_on',
            ),
        }),
    )
    formfield_overrides = {
        django.db.models.ForeignKey: {'widget': Select2},
        django.db.models.ManyToManyField: {'widget': Select2Multiple},
    }
    list_display = (
        'id',
        'page',
        'title',
        'description',
        'keywords',
        'resource_type',
        'get_image_box',
        'fb_app_id',
        'site_name',
        'twitter_site',
    )
    list_display_links = (
        'page',
    )
    readonly_fields = (
        'id',
        'created_on',
        'updated_on',
    )


@admin.register(models.SiteExtra)
class SiteExtraAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'site',
                'google_analytics_id',
                'mailchimp_api_key',
                'mailchimp_list_id',
            )
        }),
        (_('Meta data'), {
            'classes': ('collapse',),
            'fields': (
                'id',
                'created_on',
                'updated_on',
            ),
        }),
    )
    formfield_overrides = {
        django.db.models.ForeignKey: {'widget': Select2},
        django.db.models.ManyToManyField: {'widget': Select2Multiple},
    }
    list_display = (
        'get_site_id',
        'site',
        'get_site_name',
        'google_analytics_id',
        'mailchimp_api_key',
        'mailchimp_list_id',
        'updated_on',
    )
    list_display_links = (
        'site',
        'get_site_name',
    )
    readonly_fields = (
        'id',
        'created_on',
        'updated_on',
    )


@admin.register(models.Text)
class TextAdmin(ImageCroppingMixin, SortableAdminMixin, TranslationAdmin):
# class TextAdmin(ImageCroppingMixin, TranslationAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'page',
            )
        }),
        ('CharField', {
            'fields': (
                't_CharField_boolean',
                't_CharField',
                't_CharField_slug',
            )
        }),
        ('TextField', {
            'fields': (
                't_TextField_boolean',
                't_TextField',
            )
        }),
        ('ImageField', {
            'fields': (
                't_ImageField_boolean',
                't_ImageField',
                't_ImageRatioField_free',
                't_ImageRatioField_crop',
                't_ImageRatioField_square',
            )
        }),
        ('FileField', {
            'fields': (
                't_FileField_boolean',
                't_FileField',
            )
        }),
        ('EmailField', {
            'fields': (
                't_EmailField_boolean',
                't_EmailField',
            )
        }),
        ('GeopositionField', {
            'fields': (
                't_GeopositionField_boolean',
                't_GeopositionField',
            )
        }),
        ('RichTextField', {
            'fields': (
                't_RichTextField_boolean',
                't_RichTextField',
            )
        }),
        ('URLField', {
            'fields': (
                't_URLField_boolean',
                't_URLField',
            )
        }),
        ('VideoField', {
            'fields': (
                't_VideoField_boolean',
                't_VideoField_cover',
                't_VideoField_cover_cropping',
                't_VideoField_mp4',
                't_VideoField_ogg',
                't_VideoField_swf',
                't_VideoField_webm',
            )
        }),
        (_('Meta data'), {
            'classes': ('collapse',),
            'fields': (
                'id',
                'created_on',
                'updated_on',
            ),
        }),
    )
    formfield_overrides = {
        django.db.models.FileField: {'widget': widgets.ImageWidget},
        django.db.models.ForeignKey: {'widget': Select2},
        django.db.models.ManyToManyField: {'widget': Select2Multiple},
    }
    list_display = (
        'id',
        'page',
        'get_value_fr',
        'get_value_en',
        'get_value_es',
    )
    list_display_links = (
        'page',
        'get_value_fr',
    )
    list_filter = (
        'page',
    )
    readonly_fields = (
        'id',
        'created_on',
        'updated_on',
        't_CharField_slug',
    )
    search_fields = (
        'id',
        't_CharField_en',
        't_CharField_es',
        't_CharField_fr',
        't_TextField_en',
        't_TextField_es',
        't_TextField_fr',
        't_RichTextField_en',
        't_RichTextField_es',
        't_RichTextField_fr',
    )
