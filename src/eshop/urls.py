""" Urls for the eshop app """

from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

__author__ = 'Sathi, Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# URLs
urlpatterns = [
    url(
        r'^panier/$',
        views.CartView.as_view(),
        name='cart'
    ),
    url(
        r'^notification/$',
        views.payment_notification,
        name='notification'
    ),
    url(
        r'^cart/count/$',
        views.ItemCountView.as_view(),
        name='item_count'
    ),
    url(
        r'^cart/item/remove$',
        views.RemoveCartItemAPIView.as_view(),
        name='cartitem_remove_api'
    ),
    url(
        r'^check-out/$',
        views.CheckoutView.as_view(),
        name='checkout'
    ),
    url(
        r'^check-out/adresse/$',
        views.AddressSelectFormView.as_view(),
        name='order_address'
    ),
    url(
        r'^check-out/adresse/ajouter/$',
        views.UserAddressCreateView.as_view(),
        name='user_address_create'
    ),
    url(
        r'^commandes/(?P<pk>\d+)/$',
        views.order_detail,
        name='order_detail'
    ),
    url(
        r'^commandes/paiement/$',
        views.Payment,
        name='payment'
    ),
    url(
        r'^check-out/final/$',
        views.CheckoutFinalView.as_view(),
        name='checkout_final'
    ),
    url(
        r'^orders/payment/after/',  # Linked to external payment module
        views.CheckoutFinalView.as_view(),
        name='payment_after'
    ),
    url(
        r'^order/confirmation/$',
        TemplateView.as_view(template_name='eshop/email/order_confirmation_mail.html')
    ),
    url(
        r'^order/invoice/$',
        TemplateView.as_view(template_name='eshop/invoice.html')
    ),

    # API
    url(
        r'^api/cart/$',
        views.CartAPIView.as_view(),
        name='cart_api'
    ),
]
