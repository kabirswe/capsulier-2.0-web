""" Translations for the product app """

from modeltranslation.translator import register, TranslationOptions
from . import models

__author__ = 'Sathi'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Translations
@register(models.Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'description',
    )


@register(models.Feature)
class FeatureTranslationOptions(TranslationOptions):
    fields = (
        'name',
    )


@register(models.FeatureCategory)
class FeatureCategoryTranslationOptions(TranslationOptions):
    fields = (
        'name',
    )


@register(models.Product)
class ProductTranslationOptions(TranslationOptions):
    fields = (
        'name',
    )


@register(models.ProductExtra)
class ProductExtraTranslationOptions(TranslationOptions):
    fields = (
        'description',
    )


@register(models.ProductLang)
class ProductLangTranslationOptions(TranslationOptions):
    fields = (
        'description',
        'description_short',
        'description_short2',
        'description_short3',
        'meta_description',
        'meta_title',
    )


@register(models.Variation)
class VariationTranslationOptions(TranslationOptions):
    fields = (
        'title',
    )


# Old
@register(models.CustomPrice)
class CustomPriceTranslationOptions(TranslationOptions):
    fields = (
        'price',
    )
    required_languages = ('fr', )
