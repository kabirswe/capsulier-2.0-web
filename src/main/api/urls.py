""" API URLs for the main app """

from django.conf.urls import url

from . import views

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# URLs
urlpatterns = [
    url(
        r'^seo/',
        views.SEOAPI.as_view(),
        name='api_seo'
    ),
    url(
        r'^text/$',
        views.TextAPI.as_view(),
        name='api_text'
    ),
    url(
        r'^text/(?P<pk>\d+)/',
        views.TextRetrieveAPI.as_view(),
        name='api_text_detail'
    ),
]
