""" Translations for the eshop app """

from modeltranslation.translator import register, TranslationOptions

from . import models

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Translations
@register(models.PromoCode)
class PromoCodeTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'description',
    )
