""" URLs for the page app """

from django.conf.urls import url

from . import views

__author__ = 'Sathi, Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


urlpatterns = [
    url(
        r'^$',
        views.home,
        name='home'
    ),
    url(
        r'^cgv/$',
        views.cgv,
        name='cgv'
    ),
    url(
        r'^concept/$',
        views.concept,
        name='concept'
    ),
    url(
        r'^eshop/$',
        views.eshop,
        name='eshop'
    ),
    url(
        r'^faq/$',
        views.faq,
        name='faq'
    ),
    url(
        r'^legal_notice/$',
        views.legal_notice,
        name='legal_notice'
    ),
    url(
        r'^pro/$',
        views.pro,
        name='pro'
    ),
    url(
        r'^map/$',
        views.map,
        name='map'
    ),
    url(
        r'^boutiques/$',
        views.shop,
        name='shop'
    ),

    # To check
    url(
        r'^address/(?P<id>\d+)/edit/$',
        views.address_edit,
        name='address_edit'
    ),
    url(
        r'^api/shop/$',
        views.ShopAPIView.as_view(),
        name='shop_api'
    ),
]
