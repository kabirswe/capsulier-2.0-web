""" API URLs for the main app """

from django.conf.urls import url

from . import views

__author__ = 'Alamgir Kabir Roni'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# URLs
urlpatterns = [
    url(
        r'^concept/map/$',
        views.ConceptMapAPIView.as_view(),
        name='concept_map'
    ),
]
