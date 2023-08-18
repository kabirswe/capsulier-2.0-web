""" Admin for the page app """

import django.db.models

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from adminsortable2.admin import SortableAdminMixin
from easy_select2.widgets import Select2, Select2Multiple
from image_cropping import ImageCroppingMixin
from modeltranslation.admin import TranslationAdmin

from main.helpers import get_image_box, get_marker_box
from main.widgets import ImageWidget

from . import models

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Inlines
class ScheduleInline(admin.TabularInline):
    model = models.Schedule
    extra = 0
    fields = (
        'day',
        'morning_start_time',
        'morning_end_time',
        'afternoon_start_time',
        'afternoon_end_time',
        'close',
    )
    max_num = 7


class TeamMemberInline(ImageCroppingMixin, admin.TabularInline):
    model = models.TeamMember
    extra = 0
    fields = (
        'first_name',
        'last_name',
        'image',
        'image_cropping',
    )


# Admin
@admin.register(models.FAQ)
class FAQAdmin(SortableAdminMixin, TranslationAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'content',
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
        'title',
    )
    list_display_links = (
        'title',
    )
    readonly_fields = (
        'id',
        'created_on',
        'updated_on',
    )
    search_fields = (
        'title',
    )


@admin.register(models.Partner)
class PartnerAdmin(ImageCroppingMixin, SortableAdminMixin, TranslationAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'active',
                'sites',
                'image',
                'image_cropping',
                'name',
                'category',
                'description',
                'link',
            )
        }),
        (_('Meta Data'), {
            'classes': ('collapse',),
            'fields': (
                'id',
                'created_on',
                'created_by',
                'updated_on',
                'updated_by',
                'slug',
            ),
        }),
    )
    formfield_overrides = {
        django.db.models.ForeignKey: {'widget': Select2},
        django.db.models.ManyToManyField: {'widget': Select2Multiple},
    }
    list_display = (
        'active',
        get_image_box,
        'name',
        'description',
    )
    list_display_links = (
        get_image_box,
        'name',
    )
    list_filter = (
        'sites__name',
    )
    readonly_fields = (
        'id',
        'created_on',
        'created_by',
        'updated_on',
        'updated_by',
        'slug',
    )

    def save_model(self, request, obj, form, change):
        if change:
            if request.user:
                obj.updated_by = request.user
        else:
            if request.user:
                obj.created_by = request.user
                obj.updated_by = request.user
        obj.save()


@admin.register(models.Shop)
class ShopAdmin(ImageCroppingMixin, admin.ModelAdmin):
    fieldsets = (
        (_('Attributes'), {
            'fields': (
                'active',
                'sites',
            )
        }),
        (_('Shop'), {
            'fields': (
                'name',
                'logo',
                'image',
                'image_cropping',
            )
        }),
        (_('Informations'), {
            'fields': (
                'phone',
                'email',
                'website',
                'address',
                'address2',
            )
        }),
        (_('Meta Data'), {
            'classes': ('collapse',),
            'fields': (
                'id',
                'created_on',
                'created_by',
                'updated_on',
                'updated_by',
                'slug',
            ),
        }),
    )
    formfield_overrides = {
        django.db.models.FileField: {'widget': ImageWidget},
        django.db.models.ForeignKey: {'widget': Select2},
        django.db.models.ManyToManyField: {'widget': Select2Multiple},
    }
    inlines = [
        ScheduleInline,
        TeamMemberInline,
    ]
    list_display = (
        'active',
        get_image_box,
        'name',
        'email',
        'phone',
    )
    list_display_links = (
        get_image_box,
        'name',
    )
    readonly_fields = (
        'id',
        'created_on',
        'created_by',
        'updated_on',
        'updated_by',
        'slug',
    )

    def save_model(self, request, obj, form, change):
        if change:
            if request.user:
                obj.updated_by = request.user
        else:
            if request.user:
                obj.created_by = request.user
                obj.updated_by = request.user
        obj.save()


@admin.register(models.Slider)
class SliderAdmin(ImageCroppingMixin, SortableAdminMixin, TranslationAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'sites',
                'image',
                'image_cropping',
                'title',
                'button_text',
                'url',
            )
        }),
        (_('Meta Data'), {
            'classes': ('collapse',),
            'fields': (
                'id',
                'created_on',
                'created_by',
                'updated_on',
                'updated_by',
            ),
        }),
    )
    formfield_overrides = {
        django.db.models.ForeignKey: {'widget': Select2},
        django.db.models.ManyToManyField: {'widget': Select2Multiple},
    }
    list_display = (
        'get_image_box',
        'title',
        'button_text',
        'url',
        'updated_on',
        'updated_by',
    )
    list_display_links = (
        'title',
        'get_image_box',
    )
    list_filter = (
        'sites__name',
    )
    readonly_fields = (
        'id',
        'created_on',
        'created_by',
        'updated_on',
        'updated_by',
    )

    def save_model(self, request, obj, form, change):
        if change:
            if request.user:
                obj.updated_by = request.user
        else:
            if request.user:
                obj.created_by = request.user
                obj.updated_by = request.user
        obj.save()


@admin.register(models.ConceptMap)
class ConceptMapAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Shop'), {
            'fields': (
                'name',
                'marker',
                'address',
            )
        }),
        (_('Meta Data'), {
            'classes': ('collapse',),
            'fields': (
                'id',
                'created_on',
                'created_by',
                'updated_on',
                'updated_by',
            ),
        }),
    )
    list_display = (
        'name',
        get_marker_box,
        'address',
    )
    list_display_links = (
        get_marker_box,
        'name',
    )
    readonly_fields = (
        'id',
        'created_on',
        'created_by',
        'updated_on',
        'updated_by',
    )

    def save_model(self, request, obj, form, change):
        if change:
            if request.user:
                obj.updated_by = request.user
        else:
            if request.user:
                obj.created_by = request.user
                obj.updated_by = request.user
        obj.save()
