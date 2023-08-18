""" URLs for the userprofile app """

from django.conf.urls import url

from eshop import views as eshop_views

from . import views

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# URLs
urlpatterns = [
    url(
        r'^$',
        views.profile,
        name='profile'
    ),
    url(
        r'^adresse/ajouter/$',
        eshop_views.UserAddressCreateView2.as_view(),
        name='address_create'
    ),
]
