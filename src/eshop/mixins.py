""" Mixins for the eshop app """

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from . import models


# Mixins
class CartOrderMixin(object):
    def get_order(self, *args, **kwargs):
        cart = self.get_cart()
        if cart is None:
            return None
        new_order_id = self.request.session.get('order_id')
        if new_order_id is None:
            new_order = models.Order.objects.create(cart=cart)
            self.request.session['order_id'] = new_order.id
        else:
            new_order = models.Order.objects.get(id=new_order_id)
        return new_order

    def get_cart(self, *args, **kwargs):
        cart_id = self.request.session.get('cart_id')
        if cart_id is None:
            return None
        cart = models.Cart.objects.get(id=cart_id)
        if cart.items.count() <= 0:
            return None
        return cart


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs
        )
