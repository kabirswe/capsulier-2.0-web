""" Admin for the contact app """

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from import_export.admin import ExportMixin

from . import models

__author__ = 'Sathi'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Admins
@admin.register(models.Contact)
class ContactAdmin(ExportMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'email',
                'message',
            )
        }),
        (_('Meta data'), {
            'fields': (
                'id',
                'created_on',
            ),
        }),
    )
    list_display = (
        'name',
        'email',
        'message',
        'created_on',
    )
    readonly_fields = (
        'id',
        'name',
        'email',
        'message',
        'created_on',
    )
