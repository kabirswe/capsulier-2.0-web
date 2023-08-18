""" URLs for the mycaps app """

from django.conf.urls import url

from . import views

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# URLs
urlpatterns = [
    url(
        r'^$',
        views.mycaps,
        name='mycaps',
    ),
    url(
        r'^crop/$',
        views.crop,
        name='crop'
    ),
]
