""" Admin for the userprofile app """

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from . import models

__author__ = 'Alamgir Kabir Roni, Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Admin
@admin.register(models.SignUp)
class SignUpAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'user',
                'status',
            )
        }),
        (_('Private Information'), {
            'fields': (
                'gender',
                'date_of_birth',
            ),
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
        'user',
        'status',
        'gender',
    )
    list_filter = (
        'status',
        'gender',
    )
    raw_id_fields = (
        'user',
    )
    readonly_fields = (
        'id',
        'created_on',
        'updated_on',
    )
