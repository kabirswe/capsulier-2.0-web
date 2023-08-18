# pylint: disable=C0111

""" Admin for the product app """

import django.db.models

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from adminsortable2.admin import SortableAdminMixin
from easy_select2.widgets import Select2, Select2Multiple
from image_cropping import ImageCroppingMixin
from import_export.admin import ImportExportMixin
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline

from . import models

__author__ = 'Sathi, Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Inlines
class FeatureInline(admin.TabularInline):
    model = models.Feature
    extra = 0
    fields = (
        'name',
    )
    formfield_overrides = {
        django.db.models.ForeignKey: {'widget': Select2},
        django.db.models.ManyToManyField: {'widget': Select2Multiple},
    }


class ProductExtraAdminInline(ImageCroppingMixin, TranslationStackedInline):
    model = models.ProductExtra
    fields = (
        'supplier',
        'position',
        'image',
        'image_cropping',
        'background_image',
        'background_image_cropping',
        'color',
        'song_artist',
        'song_track_name',
        'description',
        'song',
    )
    formfield_overrides = {
        django.db.models.ForeignKey: {'widget': Select2},
        django.db.models.ManyToManyField: {'widget': Select2Multiple},
    }


class ProductFeatureInline(admin.TabularInline):
    model = models.ProductFeature
    extra = 0
    fields = (
        'feature',
    )
    raw_id_fields = (
        'feature',
    )


class ProductLangAdminInline(TranslationStackedInline):
    model = models.ProductLang
    fieldsets = (
        (_('Description'), {
            'classes': ('collapse',),
            'fields': (
                'description_short',
                'description_short2',
                'description_short3',
                'description',
            )
        }),
        (_('SEO'), {
            'classes': ('collapse',),
            'fields': (
                'meta_title',
                'meta_description',
            )
        }),
    )
    formfield_overrides = {
        django.db.models.ForeignKey: {'widget': Select2},
        django.db.models.ManyToManyField: {'widget': Select2Multiple},
    }


class VariationInline(TranslationStackedInline):
    model = models.Variation
    extra = 0
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'inventory',
                'tax_percentage',
                'price_public',
                'price_public_ve',
                'tax_public',
                'price_pro',
                'price_pro_ve',
                'tax_pro',
            )
        }),
        (_('Image'), {
            'classes': ('collapse',),
            'fields': (
                'image',
                'image_cropping',
            )
        }),
        (_('Properties'), {
            'classes': ('collapse',),
            'fields': (
                'active',
                'on_sales',
                'out_of_stock',
                'no_out_of_stock',
            )
        }),
        (_('Dimensions'), {
            'classes': ('collapse',),
            'fields': (
                'weight',
                'depth',
                'height',
                'width',
            )
        }),
        (_('Reference'), {
            'classes': ('collapse',),
            'fields': (
                'ean13',
                'supplier_reference',
                'upc',
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
    readonly_fields = (
        'id',
        'created_on',
        'updated_on',
        'price_public_ve',
        'tax_public',
        'price_pro_ve',
        'tax_pro',
    )


# Models
@admin.register(models.Category)
class CategoryAdmin(ImageCroppingMixin, SortableAdminMixin, TranslationAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'active',
                'title',
                'description',
                'email',
                'image',
                'image_cropping',
                'image_cropping_square',
                'image_cropping_product',
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
                'slug',
            ),
        }),
    )
    formfield_overrides = {
        django.db.models.ForeignKey: {'widget': Select2},
        django.db.models.ManyToManyField: {'widget': Select2Multiple},
    }
    list_display = (
        'get_image_box',
        'get_image_box_square',
        'title',
        'description',
    )
    list_display_links = (
        'get_image_box',
        'get_image_box_square',
        'title',
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


@admin.register(models.Feature)
class FeatureAdmin(ImportExportMixin, TranslationAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'product_feature_category',
                'name',
                'image',
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
        'name',
        'product_feature_category',
        'image_tag',
    )
    list_filter = (
        'product_feature_category',
    )
    readonly_fields = (
        'id',
        'created_on',
        'updated_on',
    )
    search_fields = (
        'name',
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


@admin.register(models.FeatureCategory)
class FeatureCategoryAdmin(ImportExportMixin, TranslationAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'category',
                'name',
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
        django.db.models.ForeignKey: {'widget': Select2},
        django.db.models.ManyToManyField: {'widget': Select2Multiple},
    }
    inlines = (
        FeatureInline,
    )
    list_display = (
        'id',
        'name',
        'category',
        'updated_on',
        'updated_by',
    )
    list_display_links = (
        'name',
    )
    list_filter = (
        'category',
    )
    readonly_fields = (
        'id',
        'created_on',
        'created_by',
        'updated_on',
        'updated_by',
    )
    search_fields = (
        'name',
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


@admin.register(models.Product)
class ProductAdmin(SortableAdminMixin, ImageCroppingMixin, TranslationAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'active',
                'sites',
                'name',
                'category',
                'related_products',
            )
        }),
        (_('Meta data'), {
            'classes': ('collapse',),
            'fields': (
                'id',
                'slug',
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
    inlines = (
        ProductLangAdminInline,
        ProductFeatureInline,
        ProductExtraAdminInline,
        VariationInline,
    )
    list_display = (
        'active',
        'get_image_box',
        'get_background_image_box',
        'name',
        'category',
        'get_variation_count',
    )
    list_display_links = (
        'get_image_box',
        'name',
        'get_background_image_box',
    )
    list_filter = (
        'sites__name',
        'productextra__position_check',
        'category',
        'productextra__supplier',
    )
    readonly_fields = (
        'id',
        'slug',
        'created_on',
        'created_by',
        'updated_on',
        'updated_by',
    )
    search_fields = (
        'name',
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


@admin.register(models.ProductFeature)
class ProductFeatureAdmin(ImportExportMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'feature',
                'product',
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
        django.db.models.ForeignKey: {'widget': Select2},
        django.db.models.ManyToManyField: {'widget': Select2Multiple},
    }
    list_display = (
        'feature',
        'product',
    )
    list_filter = (
        'product__category',
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


@admin.register(models.Supplier)
class SupplierAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'name',
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
        django.db.models.ForeignKey: {'widget': Select2},
        django.db.models.ManyToManyField: {'widget': Select2Multiple},
    }
    list_display = (
        'name',
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
    search_fields = (
        'name',
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


@admin.register(models.Variation)
class VariationAdmin(ImportExportMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'product',
                'title',
                'inventory',
                'tax_percentage',
                'price_public',
                'price_public_ve',
                'tax_public',
                'price_pro',
                'price_pro_ve',
                'tax_pro',
            )
        }),
        (_('Dimensions'), {
            'classes': ('collapse',),
            'fields': (
                'weight',
                'depth',
                'height',
                'width',
            )
        }),
        (_('Reference'), {
            'classes': ('collapse',),
            'fields': (
                'ean13',
                'supplier_reference',
                'upc',
            )
        }),
        (_('Properties'), {
            'classes': ('collapse',),
            'fields': (
                'active',
                'on_sales',
                'out_of_stock',
                'no_out_of_stock',
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
        'active',
        'on_sales',
        'out_of_stock',
        'no_out_of_stock',
        'product',
        'title',
        'inventory',
        'price_public',
        'price_pro',
        'tax_percentage',
        'updated_on',
    )
    list_display_links = (
        'product',
        'title',
    )
    list_editable = (
        'inventory',
    )
    list_filter = (
        'product__sites__name',
        'product__category',
    )
    readonly_fields = (
        'created_on',
        'id',
        'price_pro_ve',
        'price_public_ve',
        'tax_pro',
        'tax_public',
        'updated_on',
    )


# Extra
@admin.register(models.ProductExtra)
class ProductExtraAdmin(ImportExportMixin, ImageCroppingMixin, TranslationAdmin):
    formfield_overrides = {
        django.db.models.ForeignKey: {'widget': Select2},
        django.db.models.ManyToManyField: {'widget': Select2Multiple},
    }
    list_display = (
        'product',
        'supplier',
        'color',
        'position',
        'song',
    )
    list_filter = (
        'position_check',
        'product__category',
    )


@admin.register(models.ProductLang)
class ProductLangAdmin(ImportExportMixin, admin.ModelAdmin):
    formfield_overrides = {
        django.db.models.ForeignKey: {'widget': Select2},
        django.db.models.ManyToManyField: {'widget': Select2Multiple},
    }
    list_display = (
        'product',
        'description',
        'description_short',
        'description_short2',
        'description_short3',
        'meta_description',
        'meta_title',
    )
    list_filter = (
        'product__category',
    )


@admin.register(models.CustomPrice)
class CustomPriceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'price_fr',
                'customer',
                'product',
            )
        }),
        (_('Translations'), {
            'classes': ('collapse',),
            'fields': (
                'price_en',
                'price_es',
            ),
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
        django.db.models.ForeignKey: {'widget': Select2},
        django.db.models.ManyToManyField: {'widget': Select2Multiple},
    }
    list_display = (
        'customer',
        'product',
        'price',
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
        obj.save()
