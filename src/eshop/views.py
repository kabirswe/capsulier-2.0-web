# -*- coding: utf-8 -*-
# pylint: disable=E501

""" Views for the cart app """

from datetime import datetime
from decimal import Decimal
from hashlib import sha1
from itertools import chain

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView

from allauth.account.forms import LoginForm
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Variation, Product

from . import forms
from . import mixins
from . import models
from . import serializers

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Views
@login_required
def address_edit(request, id):
    address_instance = models.UserAddress.objects.get(id=id)
    if request.method == 'POST':
        form = forms.UserAddressForm(
            request.POST or None,
            request.FILES or None,
            instance=address_instance
        )
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user.usercheckout
            instance.save()
            return HttpResponseRedirect(reverse('userprofile:profile'))
    else:
        form = forms.UserAddressForm(instance=address_instance)
    context = {
        'form': form,
        'instance': address_instance,
    }
    return render(request, 'eshop/address_edit.html', context)


@login_required
def order_detail(request, pk):
    order_instance = models.Order.objects.get(pk=pk)
    if request.user.is_staff or request.user == order_instance.user_checkout.user:
        context = {
            'instance': order_instance,
        }
        return render(request, 'eshop/order_detail.html', context)
    raise Http404


# To clean
class ItemCountView(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            cart_id = self.request.session.get('cart_id')
            if cart_id is None:
                count = 0
            else:
                cart = models.Cart.objects.get(id=cart_id)
                cart_item_list = cart.cartitem_set.all()
                count = 0
                for obj in cart_item_list:
                    count += obj.quantity
            request.session['cart_item_count'] = count
            return JsonResponse({'count': count})
        else:
            raise Http404


class CartView(SingleObjectMixin, View):
    model = models.Cart

    def get_object(self, *args, **kwargs):
        self.request.session.set_expiry(0)
        cart_id = self.request.session.get('cart_id')
        if cart_id is None:
            cart = models.Cart()
            cart.save()
            cart_id = cart.id
            self.request.session['cart_id'] = cart_id
        cart = models.Cart.objects.get(id=cart_id)
        if self.request.user.is_authenticated():
            cart.user = self.request.user
            cart.save()
        return cart

    def get_price(self, instance):
        if self.request.user.is_authenticated and self.request.user.profile.status == 'b':
            return instance.price_pro
        return instance.price_public

    def cart_item_price(self, itemInstance, quantity):
        if quantity >= 1:
            price = self.get_price(itemInstance.item)
            itemInstance.unit_price = Decimal(price)
            itemInstance.save()
        itemInstance.cart.save()

    def get(self, request, *args, **kwargs):
        cart = self.get_object()
        item_id = request.GET.get('item')
        delete_item = request.GET.get('delete', False)
        remove_qty = request.GET.get('remove')
        coupon_code = request.GET.get('coupon')
        shipping_service = request.GET.get('shipping')

        # Add item
        if item_id and not remove_qty:
            item_instance = get_object_or_404(Variation, id=item_id)
            qty = request.GET.get('qty', 1)
            try:
                if int(qty) < 1:
                    delete_item = True
            except:
                raise Http404

            cart_item, created = models.CartItem.objects.get_or_create(
                cart=cart,
                item=item_instance
            )
            self.cart_item_price(cart_item, qty)
            if delete_item:
                cart_item.delete()
            else:
                if created:
                    cart_item.quantity = float(qty)
                else:
                    cart_item.quantity = float(qty) + float(cart_item.quantity)
                cart_item.save()
            if not request.is_ajax():
                return HttpResponseRedirect(reverse('eshop:cart'))

        # Remove Qty
        if remove_qty:
            item_instance = get_object_or_404(Variation, id=item_id)
            cart_item = models.CartItem.objects.get(
                cart=cart,
                item=item_instance
            )
            if cart_item.quantity == 1:
                pass
            else:
                cart_item.quantity = float(cart_item.quantity) - float(1)
                cart_item.save()
            if not request.is_ajax():
                return HttpResponseRedirect(reverse('eshop:cart'))

        # Coupon
        if coupon_code:
            try:
                coupon_object = models.PromoCode.objects.get(code=coupon_code)
                cart.promo_code = coupon_object
                cart.save()
            except:
                cart.promo_code = None
                cart.save()

        # Shipping
        if shipping_service:
            print 'shipping'
            try:
                shipping_object = models.ShippingService.objects.get(id=shipping_service)
                print shipping_object
                cart.shipping_service = shipping_object
                cart.save()
            except:
                print 'none'
                cart.shipping_service = None
                cart.save()

        # Return json data
        if item_id:
            cart_item = models.CartItem.objects.filter(cart_id=cart.id)
            cart_item2 = cart_item.get(item_id=item_id)
            if request.is_ajax():
                try:
                    line_total = cart_item2.line_item_total
                except:
                    line_total = None
                try:
                    price = cart_item2.item.price
                except:
                    price = None
                try:
                    subtotal = cart_item2.cart.subtotal
                except:
                    subtotal = None
                try:
                    promo_code = cart.promo_code.code
                except:
                    promo_code = None
                try:
                    discount_total = cart.discount_total
                except:
                    discount_total = None
                try:
                    shipping_total = cart.shipping_total
                except:
                    shipping_total = None
                try:
                    cart_total = cart_item2.cart.total
                except:
                    cart_total = None
                try:
                    tax_total = cart_item2.cart.tax_total
                except:
                    tax_total = None
                try:
                    total_items = cart_item2.cart.items.count()
                except:
                    total_items = 0

                data = {
                    'cart_total': cart_total,
                    'deleted': delete_item,
                    'discount_total': discount_total,
                    'shipping_total': shipping_total,
                    'line_total': line_total,
                    'price': price,
                    'promo_code': promo_code,
                    'subtotal': subtotal,
                    'tax_total': tax_total,
                    'total_items': total_items,
                }

                return JsonResponse(data)

        # Shipping service list for context
        shipping_service_list = models.ShippingService.objects.active().order_by('id')

        # Recommended product list for context
        current_site = get_current_site(request)
        to_exclude_list = self.get_object().items.all()
        category1_count = self.get_object().items.filter(
            product__category=1
        ).count()
        if category1_count < 3:
            related_product_list1 = Product.objects.active().filter(
                sites=current_site.id,
                category=1
            ).exclude(variation__in=to_exclude_list).order_by('?')[:1]
        else:
            related_product_list1 = ''
        related_product_list2 = Product.objects.active().filter(
            sites=current_site.id,
            category=6
        ).exclude(variation__in=to_exclude_list).order_by('?')[:1]
        related_product_list3 = Product.objects.active().filter(
            sites=current_site.id,
            category=2
        ).exclude(variation__in=to_exclude_list).order_by('?')[:1]
        related_product_list = list(chain(
            related_product_list1,
            related_product_list2,
            related_product_list3
        ))
        context = {
            'object': self.get_object(),
            'product_list': related_product_list,
            'shipping_service_list': shipping_service_list,
        }
        return render(request, 'eshop/cart.html', context)


@method_decorator(login_required, name='dispatch')
class CheckoutView(mixins.CartOrderMixin, DetailView):
    model = models.Cart
    template_name = 'eshop/checkout.html'

    def get_object(self, *args, **kwargs):
        cart = self.get_cart()
        if cart is None:
            return None
        return cart

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutView, self).get_context_data(*args, **kwargs)
        user_can_continue = False
        user_check_id = self.request.session.get('user_checkout_id')
        print 'user check id=', user_check_id
        if self.request.user.is_authenticated():
            user_can_continue = True
            user_checkout, created = models.UserCheckout.objects.get_or_create(
                email=self.request.user.email)
            user_checkout.user = self.request.user
            user_checkout.order = self.get_order()
            user_checkout.save()
            self.request.session['user_checkout_id'] = user_checkout.id
        elif not self.request.user.is_authenticated() and user_check_id is None:
            context['login_form'] = LoginForm()
            context['next_url'] = self.request.build_absolute_uri()
        else:
            pass
        context['order'] = self.get_order()
        context['user_can_continue'] = user_can_continue
        if user_check_id or self.request.user.is_authenticated():
            context['form'] = self.get_form_address()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user_checkout, created = models.UserCheckout.objects.get_or_create(
                email=email)
            request.session['user_checkout_id'] = user_checkout.id
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('eshop:checkout')

    def get(self, request, *args, **kwargs):
        get_data = super(CheckoutView, self).get(request, *args, **kwargs)
        cart = self.get_object()
        if cart is None:
            return redirect('eshop:cart')
        new_order = self.get_order()
        user_checkout_id = request.session.get('user_checkout_id')
        if user_checkout_id is not None:
            user_checkout = models.UserCheckout.objects.get(
                id=user_checkout_id
            )
            new_order.user_checkout = user_checkout
            new_order.save()

        return get_data

    def get_addresses(self, *args, **kwargs):
        user_check_id = self.request.session.get('user_checkout_id')
        user_checkout = models.UserCheckout.objects.get(id=user_check_id)

        same_address = models.UserAddress.objects.filter(
            user=user_checkout,
            types='a',
        )
        b_address = models.UserAddress.objects.filter(
            user=user_checkout,
            types='b',
        )
        s_address = models.UserAddress.objects.filter(
            user=user_checkout,
            types='s',
        )
        return same_address, b_address, s_address

    def get_form_address(self, *args, **kwargs):
        form = forms.AddressFormShipping(*args, **kwargs)
        same_address, b_address, s_address = self.get_addresses()

        if same_address.count() == 0:
            form.fields['shipping_address'].queryset = s_address
            form.fields['billing_address'].queryset = b_address
        else:
            form.fields['shipping_address'].queryset = same_address | s_address
            form.fields['billing_address'].queryset = same_address | b_address
        return form


class CheckoutFinalView(mixins.CartOrderMixin, View):

    def get(self, request, *args, **kwargs):

        q = request.GET
        print q
        order = models.Order.objects.get(id=q['vads_order_id'])
        order_total = order.order_total
        # if (int(item_instance.inventory) < int(qty)):
        #     # flash_message = 'Quantity exceed the limit'
        # else:
        cart_item = models.CartItem.objects.filter(cart_id=order.cart_id)

        for cart_item_data in cart_item:
            print 'variation id=', cart_item_data.item_id
            variation = Variation.objects.get(id=cart_item_data.item_id)

            out_of_stock = variation.out_of_stock
            no_out_of_stock = variation.no_out_of_stock
            if variation.inventory:
                remain_stock = int(variation.inventory) - int(cart_item_data.quantity)
                print 'remain_stock----------------\n'
                print remain_stock
                print '\n----------------'
                variation.inventory = (
                    remain_stock)
                if not no_out_of_stock and remain_stock <= 0:
                    variation.out_of_stock = 1
                else:
                    variation.out_of_stock = 0

                variation.save()

        if q['vads_trans_status'] == 'AUTHORISED':
            order.mark_completed(order_id=q['vads_trans_id'])
            order.send_order_mail()
            del request.session['cart_id']
            del request.session['order_id']
        else:
            return redirect('eshop:checkout')

        return redirect('eshop:order_detail', pk=order.pk)


class CartAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        queryset = models.Cart.objects.filter(id=request.session.get('cart_id'))
        serializer = serializers.CartSerializers(queryset, many=True)
        return Response(serializer.data)


class RemoveCartItemAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        q = request.GET
        if 'item_id' in q and q['item_id']:
            cart_item = models.CartItem.objects.get(
                cart_id=request.session.get('cart_id'),
                item_id=q['item_id']
            )
        else:
            cart_item = models.CartItem.objects.get(
                cart_id=request.session.get('cart_id')
            )
        cart_item.delete()

        return Response({'msg': 'Item removed successfully.'})


def build_absolute_uri(request, location):
    if getattr(settings, 'MAHDIL_LIVE', True) is True:
        scheme = request.is_secure() and 'https' or 'http'
        liveOrLocal = get_current_site(request).domain
    else:
        scheme = request.is_secure() and 'https' or 'http'
        liveOrLocal = 'localhost:8000/' + request.LANGUAGE_CODE
    return "%s://%s%s" % (scheme, liveOrLocal, location)


def get_trans_id():
    """
    Range allowed is between 000000 and 899999.
    So if we assume that there is only one transaction per seconde, that covers 86400
    unique transactions.
    And to decrease the probability of a collision between two customers at the same second
    we can use the first digit of the microsecond.

    It's not completely bulletproof because it can happen if two person confirm their order
    at the same time, same second and the same microsecond.
    """
    n = datetime.utcnow()
    return "%06d" % (n.hour * 36000 + n.minute * 600 + n.second * 10 + n.microsecond / 10000)


def ksort(d):
    return [(k, d[k]) for k in sorted(d.keys())]


# @login_required
def AfterPayment(request):
    if request.method == 'GET':
        q = request.GET
        user_checkout = models.UserCheckout.objects.get(
            order_id=q['vads_order_id'])
        order = models.Order.objects.get(id=user_checkout.order_id)
        if q['vads_trans_status'] == 'AUTHORISED':
            user_checkout.vads_operation_type = q['vads_operation_type']
            user_checkout.vads_card_number = q['vads_card_number']
            user_checkout.vads_trans_id = q['vads_trans_id']
            user_checkout.save()
            order.status = 'p'
            print 'before save'
            order.save()
            print 'after save'
            # order.send_order_mail()
            del request.session['cart_id']
            del request.session['order_id']
            del request.session['user_checkout_id']

        context = {
            'object': q,
        }
        return render(request, 'eshop/payment_after_form.html', context)


def Payment(request):
    try:
        user_check_id = request.session.get('user_checkout_id')
        order_id = request.session.get('order_id')
        order = models.Order.objects.get(id=order_id)
        user_checkout = models.UserCheckout.objects.get(id=user_check_id)
    except models.Order.DoesNotExist:
        return redirect('eshop:checkout')

    trans_id = get_trans_id()

    payment_url = 'https://paiement.systempay.fr/vads-payment/'
    shop_id = '65126625'
    if settings.PAYMENT_PRODUCTION:
        certificate = '8043856681034602'
    else:
        certificate = '2611391557047054'
    payment = {}
    payment['vads_version'] = 'V2'
    payment['vads_page_action'] = 'PAYMENT'
    payment['vads_action_mode'] = 'INTERACTIVE'
    payment['vads_payment_config'] = 'SINGLE'
    payment['vads_site_id'] = shop_id
    if settings.PAYMENT_PRODUCTION:
        payment['vads_ctx_mode'] = 'PRODUCTION'
    else:
        payment['vads_ctx_mode'] = 'TEST'
    payment['vads_trans_date'] = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    payment['vads_amount'] = int(order.order_total * 100)
    payment['vads_currency'] = '978'
    payment['vads_order_id'] = order.id
    payment['vads_cust_email'] = user_checkout.email
    payment['vads_language'] = 'fr'
    payment['vads_trans_id'] = trans_id
    payment['vads_url_return'] = build_absolute_uri(
        request, '/eshop/orders/payment/after/')
    payment['vads_redirect_success_timeout'] = 1
    payment['vads_return_mode'] = 'GET'
    # print('payment')
    # print(payment)
    """
    Compute the signature according to the doc
    """
    ksrt = ksort(payment)
    # print(ksrt)
    vs = ''
    for k in ksrt:
        # if i > 0: #this is for blocking csrf if you are going to submit this
        # from form
        vs = vs + str(k[1]) + '+'
        # i = i + 1
    vs = vs + certificate

    print 'vs', vs
    signature = sha1(vs).hexdigest()
    payment['signature'] = signature
    user_checkout.signature = payment['signature']
    user_checkout.save()
    context = {
        'form': payment,
        'payment_url': payment_url,
    }
    return render(request, 'eshop/payment_form.html', context)


def payment_notification(request):
    context = {}
    return render(request, 'eshop/notification.html', context)


class OrderList(mixins.LoginRequiredMixin, ListView):
    queryset = models.Order.objects.all()

    def get_queryset(self):
        user_check_id = self.request.user.id
        try:
            user_checkout = models.UserCheckout.objects.get(id=user_check_id)
        except models.UserCheckout.DoesNotExist:
            raise Http404
        return super(OrderList, self).get_queryset().filter(user=user_checkout)


class UserAddressCreateView(CreateView):
    form_class = forms.UserAddressForm
    template_name = 'eshop/forms.html'
    success_url = reverse_lazy('eshop:order_address')

    def get_checkout_user(self):
        user_check_id = self.request.session.get('user_checkout_id')
        if user_check_id:
            user_checkout = models.UserCheckout.objects.get(id=user_check_id)
        else:
            email = self.request.user.email
            user_checkout, created = models.UserCheckout.objects.get_or_create(
                email=email)
            self.request.session['user_checkout_id'] = user_checkout.id
        return user_checkout

    def form_valid(self, form, *args, **kwargs):
        form.instance.user = self.get_checkout_user()
        self.success_url = reverse('eshop:checkout')
        return super(UserAddressCreateView, self).form_valid(form, *args, **kwargs)


class UserAddressCreateView2(CreateView):
    form_class = forms.UserAddressForm
    template_name = 'eshop/forms.html'
    success_url = reverse_lazy('eshop:order_address')

    def get_checkout_user(self):
        user_check_id = self.request.session.get('user_checkout_id')
        if user_check_id:
            user_checkout = models.UserCheckout.objects.get(id=user_check_id)
        else:
            email = self.request.user.email
            user_checkout, created = models.UserCheckout.objects.get_or_create(
                email=email)
            self.request.session['user_checkout_id'] = user_checkout.id
        return user_checkout

    def form_valid(self, form, *args, **kwargs):
        form.instance.user = self.get_checkout_user()
        self.success_url = "%s#address" % reverse('userprofile:profile')
        return super(UserAddressCreateView2, self).form_valid(form, *args, **kwargs)


class AddressSelectFormView(mixins.CartOrderMixin, FormView):
    form_class = forms.AddressFormShipping
    template_name = 'eshop/checkout.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AddressSelectFormView,
                        self).get_context_data(*args, **kwargs)
        context['order'] = self.get_order()
        return context

    def get_addresses(self, *args, **kwargs):
        user_check_id = self.request.session.get('user_checkout_id')
        # print 'user_check_id', user_check_id
        user_checkout = models.UserCheckout.objects.get(id=user_check_id)

        same_address = models.UserAddress.objects.filter(
            user=user_checkout,
            types='a',
        )
        b_address = models.UserAddress.objects.filter(
            user=user_checkout,
            types='b',
        )
        s_address = models.UserAddress.objects.filter(
            user=user_checkout,
            types='s',
        )
        return same_address, b_address, s_address

    def get_form(self, *args, **kwargs):
        form = super(AddressSelectFormView, self).get_form(*args, **kwargs)
        same_address, b_address, s_address = self.get_addresses()

        if same_address.count() == 0:
            form.fields['billing_address'].queryset = b_address
            form.fields['shipping_address'].queryset = s_address
        else:
            form.fields['billing_address'].queryset = same_address | b_address
            form.fields['shipping_address'].queryset = same_address | s_address
        return form

    def form_valid(self, form, *args, **kwargs):
        billing_address = form.cleaned_data['billing_address']
        shipping_address = form.cleaned_data['shipping_address']
        order = self.get_order()
        order.billing_address = billing_address
        order.shipping_address = shipping_address
        order.save()
        return super(AddressSelectFormView, self).form_valid(form, *args, **kwargs)

    def get_success_url(self):
        return reverse('eshop:payment')
