""" Models for the eshop app """

from __future__ import unicode_literals

from datetime import datetime
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import pre_save, post_delete, post_save
from django.template.loader import render_to_string, get_template
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from wkhtmltopdf.utils import render_pdf_from_template

from main import models as main_models
from main.helpers import ActiveManager
from product.models import Variation

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Models
class Cart(models.Model):

    # Relations
    promo_code = models.ForeignKey(
        'PromoCode',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=_('promo code'),
    )
    items = models.ManyToManyField(
        Variation,
        through='CartItem',
        verbose_name=_('items'),
    )
    shipping_service = models.ForeignKey(
        'ShippingService',
        blank=True,
        default=1,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=_('shipping service'),
    )
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=_('user'),
    )

    # Attributes
    discount_total = models.DecimalField(
        _('discount total'),
        decimal_places=2,
        default=0,
        max_digits=10,
    )
    shipping_total = models.DecimalField(
        _('shipping total'),
        decimal_places=2,
        default=0,
        max_digits=7,
    )
    subtotal = models.DecimalField(
        _('subtotal'),
        decimal_places=2,
        default=0,
        max_digits=7,
    )
    tax_total = models.DecimalField(
        _('tax total'),
        decimal_places=2,
        default=0,
        max_digits=7,
    )
    total = models.DecimalField(
        _('total'),
        decimal_places=2,
        default=0,
        max_digits=7,
    )

    # Meta Data
    created_on = models.DateTimeField(
        _('created on'),
        auto_now_add=True,
        auto_now=False
    )
    updated_on = models.DateTimeField(
        _('updated on'),
        auto_now_add=False,
        auto_now=True
    )

    # Functions
    def __str__(self):
        return "%s" % (self.id)

    def __unicode__(self):
        return u"%s" % (self.id)

    def get_subtotal_vi(self):
        """ Return subtotal vat included """
        total = 0
        for item in self.cartitem_set.all():
            total += float(item.line_item_subtotal)
            total += float(item.line_item_tax_total)
        return "%.2f" % (total)

    def total_quantity(self):
        tq = 0
        items = self.cartitem_set.all()
        for item in items:
            tq += item.quantity
        return tq

    def save(self, *args, **kwargs):

        # Cart total calculation
        subtotal = 0
        taxtotal = 0
        total = 0
        for item in self.cartitem_set.all():
            subtotal += float(item.line_item_subtotal)
            taxtotal += float(item.line_item_tax_total)
            total += float(item.line_item_total)

        # Shipping Total
        if self.shipping_service:
            shipping_cost = self.shipping_service.shippingcost_set.filter(
                min_value__lte=subtotal,
                max_value__gte=subtotal,
            ).first()
            try:
                self.shipping_total = shipping_cost.price
                taxtotal += float(shipping_cost.tax)
                total += float(shipping_cost.price)
            except:
                self.shipping_total = 0
        else:
            self.shipping_total = 0

        # Discount calculation
        if self.promo_code:
            if self.promo_code.c_type == 'a':
                self.discount_total = float(self.total) / 100 * float(self.promo_code.percentage)
            elif self.promo_code.c_type == 'b':
                for item in self.cartitem_set.all():
                    if item.item == self.promo_code.variation:
                        self.discount_total = float(item.line_item_total) / 100 * float(self.promo_code.percentage)
            elif self.promo_code.c_type == 'c':
                item_in_cart = False
                for item in self.cartitem_set.all():
                    if item.item == self.promo_code.variation:
                        item_in_cart = True
                        self.discount_total = float(item.unit_price)
                if not item_in_cart:
                    new_var = CartItem()
                    new_var.cart = self
                    new_var.item = self.promo_code.variation
                    new_var.save()
                    self.discount_total = float(new_var.unit_price)
            total = float(total) - float(self.discount_total)
        else:
            self.discount_total = 0

        self.subtotal = "%.2f" % (subtotal)
        self.tax_total = "%.2f" % (taxtotal)
        self.total = "%.2f" % (total)
        return super(Cart, self).save(*args, **kwargs)

    # Meta
    class Meta:
        ordering = ['-created_on']
        verbose_name = _('cart')
        verbose_name_plural = _('carts')


class CartItem(models.Model):

    # Relations
    cart = models.ForeignKey(
        Cart,
        verbose_name=_('cart'),
    )
    item = models.ForeignKey(
        Variation,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=_('item'),
    )

    # Attributes
    line_item_total = models.DecimalField(
        _('total'),
        blank=True,
        decimal_places=2,
        max_digits=10,
        null=True,
        editable=False,
    )
    line_item_subtotal = models.DecimalField(
        _('subtotal'),
        blank=True,
        decimal_places=2,
        max_digits=10,
        null=True,
        editable=False,
    )
    line_item_tax_percentage = models.DecimalField(
        _('vat percentage'),
        decimal_places=3,
        default=0,
        max_digits=5,
        editable=False,
    )
    line_item_tax_total = models.DecimalField(
        _('vat total'),
        decimal_places=2,
        default=0,
        max_digits=7,
        editable=False,
    )
    unit_price = models.DecimalField(
        _('unit gross price'),
        decimal_places=2,
        max_digits=10,
        default=0,
        editable=False,
    )
    quantity = models.PositiveIntegerField(
        _('quantity'),
        default=1,
    )

    # Metadata
    created_on = models.DateTimeField(
        _('created on'),
        auto_now_add=True,
        blank=True,
        editable=False,
        null=True,
    )
    updated_on = models.DateTimeField(
        _('updated on'),
        auto_now=True,
        editable=False,
        null=True,
    )

    # Functions
    def __str__(self):
        return self.item.title

    def __unicode__(self):
        return u'%s' % (self.item.title)

    def remove(self):
        return self.item.remove_from_cart()

    def save(self, *args, **kwargs):
        self.line_item_total = float(self.quantity) * float(self.unit_price)
        self.line_item_tax_percentage = self.item.tax_percentage
        self.line_item_subtotal = float(self.line_item_total) / (1 + float(self.item.tax_percentage))
        self.line_item_tax_total = self.line_item_total - self.line_item_subtotal
        return super(CartItem, self).save(*args, **kwargs)

    # Meta
    class Meta:
        ordering = ['-updated_on']
        verbose_name = _('cart item')
        verbose_name_plural = _('cart items')


class InvoiceNumber(models.Model):

    # Attributes
    ending_date = models.DateField(
        _('ending date'),
        default=timezone.now
    )
    last_used_number = models.CharField(
        _('last used number'),
        editable=False,
        max_length=20,
    )
    number_places = models.PositiveSmallIntegerField(
        _('number places'),
        default=2,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(2)
        ]
    )
    prefix = models.CharField(
        _('prefix'),
        max_length=10
    )
    starting_date = models.DateField(
        _('starting date'),
        default=timezone.now,
    )

    # Meta Data
    created_on = models.DateTimeField(
        _('created on'),
        auto_now_add=True,
        editable=False,
        help_text=_("The object's creation date/time"),
        null=True,
    )
    updated_on = models.DateTimeField(
        _('updated on'),
        auto_now=True,
        editable=False,
        help_text=_("The object's last update date/time"),
        null=True,
    )

    # Meta
    class Meta:
        verbose_name = _('invoice number')
        verbose_name_plural = _('invoice numbers')
        indexes = [
            models.Index(fields=['created_on']),
            models.Index(fields=['updated_on']),
        ]

    # Methods
    def __str__(self):
        return "%s - %s" % (self.id, self.prefix)

    def __unicode__(self):
        return u"%s - %s" % (self.id, self.prefix)

    @staticmethod
    def get_next_invoice_number(save=False):
        number = InvoiceNumber.objects.filter(
            starting_date__lte=datetime.now(),
            ending_date__gte=datetime.now()
        ).first()
        if not number:
            return None
        return number.get_next_number(save)

    def get_next_number(self, save=False):
        if not self.last_used_number:
            return None
        last_number = int(self.last_used_number[len(self.prefix):])
        format_str = "%0" + str(len(self.last_used_number) - len(self.prefix)) + "d"
        next_number = format_str % (last_number + 1)
        if save:
            self.last_used_number = "%s%s" % (self.prefix, next_number)
            self.save()
        return "%s%s" % (self.prefix, next_number)

    def save(self, *args, **kwargs):
        if not self.last_used_number:
            self.last_used_number = self.prefix
            for index in range(self.number_places):
                self.last_used_number += '0'
        return super(InvoiceNumber, self).save(*args, **kwargs)


class Order(models.Model):

    # Choices
    ORDER_STATUS_CHOICES = (
        ('c', _('Created')),
        ('x', _('Cancel')),
        ('i', _('Invoiced')),
        ('p', _('Paid')),
        ('s', _('Shipped')),
    )

    # Relations
    billing_address = models.ForeignKey(
        'UserAddress',
        null=True,
        on_delete=models.PROTECT,
        related_name='billing_address',
        verbose_name=_('billing address'),
    )
    cart = models.ForeignKey(
        Cart,
        on_delete=models.PROTECT,
        related_name='+',
        verbose_name=_('cart'),
    )
    shipping_address = models.ForeignKey(
        'UserAddress',
        null=True,
        on_delete=models.PROTECT,
        related_name='shipping_address',
        verbose_name=_('shipping address'),
    )
    user_checkout = models.ForeignKey(
        'UserCheckout',
        null=True,
        on_delete=models.PROTECT,
        related_name='+',
        verbose_name=_('user checkout'),
    )

    # Attributes
    canceled_on = models.DateTimeField(
        _('canceled on'),
        blank=True,
        editable=False,
        help_text=_("The order cancel date"),
        null=True,
    )
    invoice_number = models.CharField(
        _('invoice number'),
        blank=True,
        editable=False,
        max_length=20,
    )
    invoiced_on = models.DateTimeField(
        _('invoiced on'),
        blank=True,
        editable=False,
        help_text=_("The order posting date"),
        null=True,
    )
    order_id = models.CharField(
        _('order id'),
        blank=True,
        max_length=20,
    )
    order_total = models.DecimalField(
        _('order total'),
        decimal_places=2,
        max_digits=7,
    )
    shipping_number = models.CharField(
        _('shipping number'),
        blank=True,
        max_length=20,
    )
    shipped_on = models.DateTimeField(
        _('shipped on'),
        blank=True,
        help_text=_("The order shipping date"),
        null=True,
    )
    status = models.CharField(
        _('status'),
        choices=ORDER_STATUS_CHOICES,
        default='c',
        max_length=1,
    )

    # Meta Data
    created_on = models.DateTimeField(
        _('created on'),
        auto_now_add=True,
        auto_now=False
    )

    # Functions
    def __str__(self):
        return self.cart.id

    def __unicode__(self):
        return u'%s' % (self.cart.id)

    def cancel(self):
        if self.status == 'x' or self.status == 'i':
            return False
        self.status = 'x'
        self.canceled_on = datetime.now()
        self.save()

    def get_absolute_url(self):
        return reverse('eshop:order_detail', kwargs={'pk': self.pk})

    def invoice(self):

        # We should only process sales headers in paid or shipping statuses
        if self.status != 'p' and self.status != 's':
            return False

        # We should skip header in shipping status
        # If they do not have a shipping number
        # (We can still be waiting for shipping agent confirmation)
        if (self.status == 's' or self.status == 'p') and self.shipping_number == '':
            return False

        # Invoice sales header
        self.invoice_number = InvoiceNumber.get_next_invoice_number(True)
        self.status = 'i'
        self.invoiced_on = datetime.now()
        self.save()
        return True

    def mark_completed(self, order_id=None):
        self.status = 'p'
        if order_id and not self.order_id:
            self.order_id = order_id
        self.save()

    def send_order_mail(self):
        ctx = {
            'text_list': main_models.Text.objects.all(),
            'order_instance': self,
        }
        msg_plain = render_to_string(
            'eshop/email/order_confirmation_mail.txt',
            ctx
        )
        msg_html = render_to_string(
            'eshop/email/order_confirmation_mail.html',
            ctx
        )
        subject = _('Subject')
        message = 'message text'
        from_email = 'contact@conservatoireducafe.fr'
        to_list = [self.user_checkout.email]
        send_mail(
            subject,
            message,
            from_email,
            to_list,
            html_message=msg_html,
            fail_silently=True
        )

    def to_pdf(self):
        # Header must be invoiced
        if self.status != 'i':
            return None
        return render_pdf_from_template(
            get_template('eshop/invoice.html'),
            None,
            None,
            {'invoice': self}
        )

    def save(self, *args, **kwargs):
        if self.status != 'i' and self.shipping_number != '' and self.shipped_on is not None:
            self.status = 's'
        return super(Order, self).save(*args, **kwargs)

    # Meta
    class Meta:
        ordering = ['-created_on', '-id']
        verbose_name = _('order')
        verbose_name_plural = _('orders')


class PromoCode(models.Model):

    # Manager
    objects = ActiveManager()

    # Choices
    TYPE_CHOICES = (
        ('a', _('Percentage on Cart Total')),
        ('b', _('Percentage on Product Variant')),
        ('c', _('Free Product Variant')),
    )

    # Relations
    variation = models.ForeignKey(
        Variation,
        blank=True,
        null=True,
        verbose_name=_('variation'),
    )

    # Attributes
    active = models.BooleanField(
        _('active'),
        default=True,
    )
    c_type = models.CharField(
        _('type'),
        choices=TYPE_CHOICES,
        max_length=1,
    )
    description = models.TextField(
        _('description'),
        blank=True,
    )
    name = models.CharField(
        _('name'),
        max_length=40,
    )
    code = models.CharField(
        _('code'),
        max_length=40,
        unique=True,
    )
    percentage = models.DecimalField(
        _('discount percentage'),
        blank=True,
        null=True,
        decimal_places=2,
        help_text=_('in %'),
        max_digits=5,
    )

    # Meta Data
    created_on = models.DateTimeField(
        _('created on'),
        auto_now_add=True,
        blank=True,
        editable=False,
        null=True,
    )
    created_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name='+',
        verbose_name=_('created by'),
    )
    updated_on = models.DateTimeField(
        _('updated on'),
        auto_now=True,
        editable=False,
        null=True,
    )
    updated_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name='+',
        verbose_name=_('updated by'),
    )

    # Meta
    class Meta:
        verbose_name = _('Promo Code')
        verbose_name_plural = _('Promo Codes')

    # Functions
    def __str__(self):
        return "%s - %s" % (self.name, self.id)

    def __unicode__(self):
        return u"%s - %s" % (self.name, self.id)


class ShippingCost(models.Model):

    # Relations
    shipping_service = models.ForeignKey(
        'ShippingService',
        verbose_name=_('shippping service')
    )

    # Attributes
    max_value = models.DecimalField(
        _('max cart value'),
        decimal_places=2,
        max_digits=10,
        help_text=_('Euro TTC'),
    )
    min_value = models.DecimalField(
        _('min cart value'),
        decimal_places=2,
        max_digits=10,
        help_text=_('Euro TTC'),
    )
    price = models.DecimalField(
        _('price'),
        decimal_places=2,
        max_digits=10,
    )
    price_ve = models.DecimalField(
        _('price vat excluded'),
        decimal_places=2,
        max_digits=10,
    )
    tax_percentage = models.DecimalField(
        _('vat percentage'),
        decimal_places=3,
        default=0.2,
        max_digits=5
    )
    tax = models.DecimalField(
        _('vat'),
        decimal_places=2,
        default=0,
        editable=False,
        max_digits=5,
    )

    # Meta Data
    created_on = models.DateTimeField(
        _('created on'),
        auto_now_add=True,
        editable=False,
        null=True,
    )
    updated_on = models.DateTimeField(
        _('updated on'),
        auto_now=True,
        editable=False,
        null=True,
    )

    # Meta
    class Meta:
        verbose_name = _('Shipping Cost')
        verbose_name_plural = _('Shipping Costs')

    # Functions
    def __str__(self):
        return "%s - %s" % (self.shipping_service.name, self.id)

    def __unicode__(self):
        return u"%s - %s" % (self.shipping_service.name, self.id)

    def save(self, *args, **kwargs):
        self.price_ve = self.price / (1 + self.tax_percentage)
        self.tax = self.price - self.price_ve
        return super(ShippingCost, self).save(*args, **kwargs)


class ShippingService(models.Model):

    # Manager
    objects = ActiveManager()

    # Attributes
    active = models.BooleanField(
        _('active'),
        default=True,
    )
    name = models.CharField(
        _('name'),
        max_length=40,
    )

    # Meta Data
    created_on = models.DateTimeField(
        _('created on'),
        auto_now_add=True,
        editable=False,
        null=True,
    )
    updated_on = models.DateTimeField(
        _('updated on'),
        auto_now=True,
        editable=False,
        null=True,
    )

    # Meta
    class Meta:
        ordering = ['name']
        verbose_name = _('Shipping Service')
        verbose_name_plural = _('Shipping Services')

    # Functions
    def __str__(self):
        return "%s" % (self.name)

    def __unicode__(self):
        return u"%s" % (self.name)


class UserCheckout(models.Model):

    # Relations
    user = models.OneToOneField(
        User,
        verbose_name=_('user'),
        null=True,
        blank=True
    )

    # Attributes
    email = models.EmailField(
        _('email'),
        unique=True,
        null=True,
        blank=True
    )

    # Functions
    def __str__(self):
        return '%s' % (self.email)

    def __unicode__(self):
        return u'%s' % (self.email)


class UserAddress(models.Model):

    # Choices
    ADDRESS_TYPE = (
        ('b', _('Billing')),
        ('s', _('Shipping')),
        ('a', _('Both')),
    )

    # Relations
    user = models.ForeignKey(
        UserCheckout,
        verbose_name=_('user'),
    )

    # Attributes
    city = models.CharField(
        _('city'),
        max_length=120
    )
    phone_number = models.CharField(
        _('phone number'),
        blank=True,
        max_length=80,
    )
    state = models.CharField(
        _('country'),
        max_length=120
    )
    street = models.CharField(
        _('street'),
        max_length=120
    )
    types = models.CharField(
        _('type'),
        choices=ADDRESS_TYPE,
        max_length=120,
    )
    zipcode = models.CharField(
        _('zip code'),
        max_length=120
    )

    # Functions
    def __str__(self):
        return "%s - %s %s - %s" % (
            self.street,
            self.zipcode,
            self.city,
            self.state
        )

    def __unicode__(self):
        return u"%s - %s %s - %s" % (
            self.street,
            self.zipcode,
            self.city,
            self.state
        )

    def get_address(self):
        return "%s, %s, %s %s" % (
            self.street,
            self.city,
            self.state,
            self.zipcode
        )


# Signals
def cart_item_post_delete_receiver(sender, instance, *args, **kwargs):
    instance.cart.save()


post_delete.connect(cart_item_post_delete_receiver, sender=CartItem)


def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
    instance.cart.save()


post_save.connect(cart_item_post_save_receiver, sender=CartItem)


def order_pre_save(sender, instance, *args, **kwargs):
    cart_total = instance.cart.total
    order_total = Decimal(cart_total)
    instance.order_total = order_total


pre_save.connect(order_pre_save, sender=Order)
