""" Translations for the main app """

from modeltranslation.translator import register, TranslationOptions

from . import models

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Translations
@register(models.Page)
class PageTranslationOptions(TranslationOptions):
    fields = (
        'name',
    )


@register(models.SEO)
class SEOTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'description',
        'keywords',
    )


@register(models.Text)
class TextTranslationOptions(TranslationOptions):
    fields = (
        't_CharField',
        't_TextField',
        't_RichTextField',
    )
