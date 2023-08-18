""" Utils for the main app """

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from . import models
from . import helpers

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# SEO
def get_seo(seo_id):
    try:
        seo = models.SEO.objects.get(id=seo_id)
    except ObjectDoesNotExist:
        seo = models.SEO.objects.get(id=1)
    except ObjectDoesNotExist:
        seo = None
    return seo


def get_seo_description(description_field):
    if description_field:
        return description_field
    seo_main = get_object_or_404(models.SEO, id=1)
    return seo_main.description


def get_seo_image(image_field, cropping_field):
    if image_field:
        return helpers.get_image(image_field, cropping_field, 1200)
    seo_main = get_object_or_404(models.SEO, id=1)
    return helpers.get_image(seo_main.image, seo_main.image_cropping, 1200)


def get_seo_title(title_field):
    if title_field:
        return title_field
    seo_main = get_object_or_404(models.SEO, id=1)
    return seo_main.title
