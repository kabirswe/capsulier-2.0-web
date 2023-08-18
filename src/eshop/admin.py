""" Admin for the eshop app """

import django.db.models

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from easy_select2.widgets import Select2, Select2Multiple
from modeltranslation.admin import TranslationAdmin

from eshop.models import Cart
from mahdil.variables.env_variables import DEBUG
from main.helpers import make_active, make_inactive

from . import models
from . import utils

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Inlines
class CartItemInline(admin.TabularInline):
    model = models.CartItem
    extra = 0
    fields = (
        'item',
        'quantity',
        'unit_price',
        'line_item_subtotal',
        'line_item_tax_percentage',
        'line_item_tax_total',
        'line_item_total',
    )

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.get_fields()]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        if not DEBUG:
            return False
        return True


# Admin
@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Cart'), {
            'fields': (
                'id',
                'created_on',
                'updated_on',
                'items',
            )
        }),
        (_('User'), {
            'fields': (
                'user',
            )
        }),
        (_('Shipping'), {
            'fields': (
                'shipping_service',
                'shipping_total',
            )
        }),
        (_('Discount'), {
            'fields': (
                'promo_code',
                'discount_total',
            )
        }),
        (_('Values'), {
            'fields': (
                'subtotal',
                'shipping_total',
                'tax_total',
                'discount_total',
                'total',
            )
        }),
    )
    inlines = [
        CartItemInline
    ]
    list_display = (
        'id',
        'created_on',
        'updated_on',
        'user',
        'total_quantity',
        'subtotal',
        'shipping_service',
        'shipping_total',
        'tax_total',
        'discount_total',
        'total',
    )
    list_display_links = (
        'id',
        'created_on',
        'updated_on',
    )
    list_filter = (
        'created_on',
        'updated_on',
    )
    readonly_fields = (
        'items',
    )

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.get_fields()]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        if not DEBUG:
            return False
        return True


@admin.register(models.InvoiceNumber)
class InvoiceNumberAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'prefix',
                'number_places',
                'starting_date',
                'ending_date',
                'last_used_number',
                'get_next_number',
            )
        }),
        (_('Meta data'), {
            'classes': ('collapse',),
            'fields': (
                'created_on',
                'updated_on'
            ),
        }),
    )
    list_display = (
        'prefix',
        'last_used_number',
        'get_next_number',
        'starting_date',
        'ending_date',
    )
    list_filter = (
        'starting_date',
        'ending_date',
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return (
                'prefix',
                'number_places',
                'last_used_number',
                'get_next_number',
                'created_on',
                'updated_on'
            )
        else:
            return (
                'last_used_number',
                'get_next_number',
                'created_on',
                'updated_on'
            )

    def get_next_number(self, obj):
        return obj.get_next_number(False)
    get_next_number.allow_tags = True
    get_next_number.short_description = _('Next number')


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    actions = (
        utils.cancel,
        utils.invoice,
        utils.print_invoice,
    )
    fieldsets = (
        (_('User'), {
            'fields': (
                'user_checkout',
                'billing_address',
                'shipping_address',
            )
        }),
        (_('Order'), {
            'fields': (
                'status',
                'id',
                'order_id',
                'created_on',
                'canceled_on',
                'cart',
                'order_total',
            )
        }),
        (_('Shipping'), {
            'fields': (
                'shipping_number',
                'shipped_on',
            )
        }),
        (_('Invoice'), {
            'fields': (
                'invoice_number',
                'invoiced_on',
            )
        }),
    )
    list_display = (
        'status',
        'id',
        'order_id',
        'created_on',
        'cart',
        'user_checkout',
        # 'billing_address',
        # 'shipping_address',
        'order_total',
        'shipping_number',
        'shipped_on',
        'invoice_number',
        'invoiced_on',
    )
    list_display_links = (
        'id',
        'order_id',
        'created_on',
    )
    list_filter = (
        'status',
        'created_on',
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = (
            'id',
            'billing_address',
            'canceled_on',
            'cart',
            'created_on',
            'invoice_number',
            'invoiced_on',
            'order_id',
            'order_total',
            'shipping_address',
            'status',
            'user_checkout',
        )
        if obj:
            if obj.status == 's' or obj.status == 'i':
                readonly_fields += (
                    'shipping_number',
                    'shipped_on',
                )
        return readonly_fields

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        if not DEBUG:
            return False
        return True


@admin.register(models.PromoCode)
class PromoCodeAdmin(TranslationAdmin):
    actions = (
        make_active,
        make_inactive,
    )
    fieldsets = (
        (_('Cart'), {
            'fields': (
                'active',
                'c_type',
                'name',
                'code',
                'percentage',
                'variation',
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
        'active',
        'c_type',
        'name',
        'code',
        'variation',
        'percentage',
    )
    list_display_links = (
        'c_type',
        'name',
        'code',
        'variation',
    )
    list_filter = (
        'c_type',
    )
    readonly_fields = (
        'id',
        'created_on',
        'created_by',
        'updated_on',
        'updated_by',
    )

    def has_delete_permission(self, request, obj=None):
        if Cart.objects.filter(promo_code=obj).count() == 0:
            return True
        return False

    def save_model(self, request, obj, form, change):
        if change:
            if request.user:
                obj.updated_by = request.user
        else:
            if request.user:
                obj.created_by = request.user
                obj.updated_by = request.user
        obj.save()


@admin.register(models.ShippingCost)
class ShippingCostAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'shipping_service',
                'min_value',
                'max_value',
                'price',
                'price_ve',
                'tax_percentage',
                'tax',
            )
        }),
        (_('Meta Data'), {
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
        'shipping_service',
        'min_value',
        'max_value',
        'price',
        'price_ve',
        'tax_percentage',
        'tax',
    )
    readonly_fields = (
        'id',
        'created_on',
        'updated_on',
        'tax',
        'price_ve',
    )


@admin.register(models.ShippingService)
class ShippingServiceAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Cart'), {
            'fields': (
                'active',
                'name',
            )
        }),
        (_('Meta Data'), {
            'classes': ('collapse',),
            'fields': (
                'id',
                'created_on',
                'updated_on',
            ),
        }),
    )
    list_display = (
        'active',
        'name',
    )
    list_filter = (
        'active',
    )
    readonly_fields = (
        'id',
        'created_on',
        'updated_on',
    )


@admin.register(models.UserCheckout)
class UserCheckoutAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Cart'), {
            'fields': (
                'user',
                'email',
            )
        }),
    )
    list_display = (
        'user',
        'email',
    )
    list_display_links = (
        'user',
        'email',
    )
    raw_id_fields = (
        'user',
    )


@admin.register(models.UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Cart'), {
            'fields': (
                'user',
                'city',
                'phone_number',
                'state',
                'street',
                'types',
                'zipcode',
            )
        }),
    )
    list_display = (
        'types',
        'user',
        'phone_number',
        'street',
        'zipcode',
        'city',
        'state',
    )
    list_display_links = (
        'types',
        'user',
    )
    readonly_fields = (
        'user',
    )
