""" Translations for the page app """

from modeltranslation.translator import register, TranslationOptions

from . import models

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Translations
@register(models.FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = (
        'content',
        'title',
    )


@register(models.Partner)
class PartnerTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'category',
        'description',
    )


@register(models.Slider)
class SliderTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'button_text',
    )
