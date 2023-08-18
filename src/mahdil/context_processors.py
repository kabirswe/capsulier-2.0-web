""" Context processors for the Mahdil project """

import uuid

from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from mahdil.settings import (
    DEBUG,
    GEOPOSITION_GOOGLE_MAPS_API_KEY,
    LIVE_TEST,
    MAHDIL_LIVE,
)

from contact.forms import ContactForm, NewsletterForm
from main.models import Text, SEO
from product import models as product_models

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Context processors
def mahdil_processor(request):
    scheme = request.is_secure() and 'https' or 'http'
    current_site = get_current_site(request)
    try:
        seo_main = SEO.objects.get(id=1)
    except ObjectDoesNotExist:
        seo_main = None
    try:
        GOOGLE_ANALYTICS_ID = current_site.siteextra.google_analytics_id
    except ObjectDoesNotExist:
        GOOGLE_ANALYTICS_ID = None
    text_list = Text.objects.all()
    if DEBUG:
        v = '?v=%s' % (uuid.uuid4())
    else:
        v = '?v=6'
    if MAHDIL_LIVE or LIVE_TEST:
        live_test = True
    else:
        live_test = False
    navbar_category_list = product_models.Category.objects.filter(
        Q(id=3) |
        Q(id=4) |
        Q(id=2) |
        Q(id=5)
    )
    context = {
        'c_form': ContactForm(),
        'n_form': NewsletterForm(),
        'current_site': current_site,
        'GEOPOSITION_GOOGLE_MAPS_API_KEY': GEOPOSITION_GOOGLE_MAPS_API_KEY,
        'GOOGLE_ANALYTICS_ID': GOOGLE_ANALYTICS_ID,
        'live_test': live_test,
        'scheme': scheme,
        'seo_main': seo_main,
        'text_list': text_list,
        'navbar_category_list': navbar_category_list,
        'v': v,
    }
    return context
