""" Admin for the blog app """

import django.db.models

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from adminsortable2.admin import SortableInlineAdminMixin
from easy_select2.widgets import Select2, Select2Multiple
from image_cropping import ImageCroppingMixin
from modeltranslation.admin import TranslationAdmin

from . import models

__author__ = 'Alamgir Kabir Roni, Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Inlines
class PostImageInline(SortableInlineAdminMixin, ImageCroppingMixin, admin.TabularInline):
    model = models.Image
    extra = 0


# Admin
@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'first_name',
                'last_name',
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
    list_display = (
        'first_name',
        'last_name',
        'updated_on',
        'updated_by',
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


@admin.register(models.Post)
class PostAdmin(TranslationAdmin):
    fieldsets = (
        (_('Attributes'), {
            'fields': (
                'active',
                'sites',
                'published_date',
            )
        }),
        (_('Article'), {
            'fields': (
                'title',
                'author',
                'abstract',
                'content',
                'credit_photo',
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
    inlines = [
        PostImageInline,
    ]
    list_display = (
        'active',
        'title',
        'published_date',
        'updated_by',
    )
    list_display_links = (
        'title',
    )
    list_filter = (
        'active',
        'sites',
    )
    readonly_fields = (
        'id',
        'created_on',
        'created_by',
        'updated_on',
        'updated_by',
        'slug',
    )
    search_fields = (
        'title',
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
