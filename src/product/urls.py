""" Urls for the product app """

from django.conf.urls import url

from . import views

__author__ = 'S. M. Sazedul Haque, Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


urlpatterns = [
    url(
        r'^$',
        views.product_list,
        name='product_list'
    ),
    url(
        r'^(?P<slug>[\w-]+)/$',
        views.product_detail,
        name='product_detail'
    ),
    url(
        r'^categorie/(?P<slug>[\w-]+)/$',
        views.category_detail,
        name='category_detail'
    ),

    # API
    url(
        r'^api/product/list/$',
        views.ProductAPIView.as_view(),
        name='api_product_list'
    ),
]
