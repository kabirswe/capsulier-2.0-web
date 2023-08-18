""" API URLs for the catalog app """

from django.conf.urls import url

from . import views

__author__ = 'Sathi'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# URLs
urlpatterns = [

    url(
        r'^products/$',
        views.ProductList.as_view(),
        name='product_list'
    ),

]
