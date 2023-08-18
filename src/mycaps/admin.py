""" Admin for the mycaps app """

import django.db.models

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from main.widgets import ImageWidget

from . import models

__author__ = 'Alamgir Kabir Roni, Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Admin
@admin.register(models.Color)
class ColorAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'color',
                'image',
                'color_image',
                'package_image',
                'background_image',
            )
        }),
        (_('Meta data'), {
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
        django.db.models.FileField: {'widget': ImageWidget},
    }
    list_display = (
        'name',
        'color',
        'get_image_box',
        'get_image_box_color',
        'get_image_box_package',
        'get_image_box_background',
    )
    list_display_links = (
        'name',
        'color',
        'get_image_box',
        'get_image_box_color',
        'get_image_box_package',
        'get_image_box_background',
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


@admin.register(models.Coffee)
class CoffeeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'description',
                'image',
            )
        }),
        (_('Meta data'), {
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
        'title',
        'description',
        'get_image_box',
        'updated_on',
        'updated_by',
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


# Admin
@admin.register(models.Package)
class PackageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'coffee',
                'color',
                'product',
                'image',
                'image1',
                'text1',
                'text2',
                'active',
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
    list_display = (
        'coffee',
        'color',
        'product',
        'get_image_box',
        'get_image_box2',
        'text1',
        'text2',
        'active',
    )
    readonly_fields = (
        'id',
        'created_on',
        'updated_on',
    )
