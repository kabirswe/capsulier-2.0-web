""" Translations for the blog app """

from modeltranslation.translator import register, TranslationOptions

from . import models

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Translations
@register(models.Post)
class PostTranslationOptions(TranslationOptions):
    fields = (
        'abstract',
        'content',
        'title',
    )
