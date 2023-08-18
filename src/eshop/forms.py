# pylint: disable=no-member
# pylint: disable=C0111

""" Forms for the eshop app """

from django import forms
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from . import models

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Forms
class AddressForm(forms.Form):
    shipping_address = forms.ModelChoiceField(
        queryset=models.UserAddress.objects.filter(types='s'),
        widget=forms.RadioSelect,
        empty_label=None,
    )
    billing_address = forms.ModelChoiceField(
        queryset=models.UserAddress.objects.filter(types='b'),
        widget=forms.RadioSelect,
        empty_label=None
    )


class AddressFormShipping(forms.Form):
    shipping_address = forms.ModelChoiceField(
        queryset=models.UserAddress.objects.filter(types='s'),
        widget=forms.RadioSelect,
        empty_label=None,
        label=_('Shipping address')
    )
    billing_address = forms.ModelChoiceField(
        queryset=models.UserAddress.objects.filter(types='b'),
        widget=forms.RadioSelect,
        empty_label=None,
        label=_('Billing address')
    )


class UserAddressForm(forms.ModelForm):

    # Choices
    ADDRESS_TYPE = (
        ('b', _('Billing')),
        ('s', _('Shipping')),
        ('a', _('Both')),
    )

    types = forms.ChoiceField(
        choices=ADDRESS_TYPE,
        label=_('Address type'),
        widget=forms.RadioSelect(),
    )

    class Meta:
        model = models.UserAddress
        fields = [
            'street',
            'zipcode',
            'city',
            'state',
            'types',
        ]


CARDNETWORK_CHOICES = (
    ('MASTERCARD', 'MasterCard'),
    ('MAESTRO', 'Maestro'),
    ('VISA', 'Visa'),
    ('CB', 'CB'),
    ('E-CARTEBLEUE', 'e-Cartebleue'),
)


class PaymentForm(forms.Form):
    cardNetwork = forms.ChoiceField(
        required=True,
        widget=forms.RadioSelect,
        choices=CARDNETWORK_CHOICES,
    )
    cardNumber = forms.IntegerField(
        label='Card Number',
        max_value=9999999999999999
    )
    cvv = forms.IntegerField(
        label='CVV',
        max_value=999
    )
    cardExpirationDate = forms.DateField(
        label=_('Card Expiration Date'),
        initial=timezone.now().date(),
        # input_formats=['%Y/%m/%d'],
        widget=forms.DateInput(format='%Y/%m/%d'),
        input_formats=('%Y/%m/%d')
    )


class PaymentBySubmitForm(forms.Form):

    #################
    # Required params
    #

    # ACTION_MODE_INTERACTIVE, ACTION_MODE_SILENT = ('INTERACTIVE', 'SILENT')
    # ACTION_MODE_CHOICES = (
    #     (ACTION_MODE_INTERACTIVE, 'INTERACTIVE'),
    #     (ACTION_MODE_SILENT, 'SILENT'),
    # )
    # vads_action_mode = forms.ChoiceField(choices=ACTION_MODE_CHOICES)

    # NB: expressed in cents for euros (unity undivisible)
    vads_amount = forms.CharField(max_length=12)
    # 978 stands for EURO (ISO 4217)
    vads_currency = forms.CharField(max_length=3)

    # CONTEXT_TEST, CONTEXT_PRODUCTION = ('TEST', 'PRODUCTION')
    # CONTEXT_CHOICES = (
    #     (CONTEXT_TEST, u'TEST'),
    #     (CONTEXT_PRODUCTION, u'PRODUCTION')
    # )
    # vads_ctx_mode = forms.ChoiceField(choices=CONTEXT_CHOICES)

    # # needs to be formated as SINGLE or MULTI:first=val1;count=val2;period=val3
    # # example: MULTI:first=5000;count=3;period=30
    # #          would represent a payment segmented with a first account of 50,00
    # #          then the rest of the amount would be divided in (count-1) other payments
    # #          with a timelapse of 30 days between them
    # #
    # # NB: if the validity date of the credit card can't handle the last payment (in case of multi)
    # #     the whole transaction will be rejected
    # vads_payment_config = forms.CharField(max_length=127)

    # vads_site_id = forms.CharField(min_length=8, max_length=8)

    # # Need to respect the format ``YYYYMMDDHHMMSS`` in UTC timezone
    # vads_trans_date = forms.CharField(min_length=14, max_length=14)

    # # Unique identifier in the range 000000 to 899999. Integer between 900000 and 999999 are reserved
    # # NB: it should only be unique over the current day
    # vads_trans_id = forms.CharField(min_length=6, max_length=6)
    # vads_version = forms.CharField(max_length=8)
    # signature = forms.CharField(min_length=40, max_length=40)

    #################
    # Optional params
    #

    # vads_capture_delay = forms.CharField(max_length=3, required=False)

    vads_cust_address = forms.CharField(max_length=255, required=False)
    vads_cust_country = forms.CharField(max_length=2, required=False)
    vads_cust_email = forms.CharField(max_length=127, required=False)
    vads_cust_id = forms.CharField(max_length=63, required=False)
    vads_cust_name = forms.CharField(max_length=127, required=False)
    # vads_cust_cell_phone = forms.CharField(max_length=32, required=False)
    vads_cust_phone = forms.CharField(max_length=32, required=False)
    # vads_cust_title = forms.CharField(max_length=63, required=False)
    vads_cust_city = forms.CharField(max_length=63, required=False)
    # vads_cust_status = forms.CharField(max_length=63, required=False)
    # vads_cust_state = forms.CharField(max_length=63, required=False)
    vads_cust_zip = forms.CharField(max_length=63, required=False)
    # vads_language = forms.CharField(max_length=2, required=False)

    vads_order_id = forms.CharField(max_length=32, required=False)
    # vads_order_info = forms.CharField(max_length=255, required=False)
    # vads_order_info2 = forms.CharField(max_length=255, required=False)
    # vads_order_info3 = forms.CharField(max_length=255, required=False)

    # vads_validation_mode = forms.CharField(max_length=1, required=False)

    def signature_params(self, data):
        raise NotImplementedError

    def sorted_signature_params(self, data):
        return sorted(p for p in self.signature_params(data) if p.startswith('vads_'))

    def values_for_signature(self, data):
        # print('values_for_signature')
        # print(data)
        l = map(unicode, (data.get(param, '')
                          for param in self.sorted_signature_params(data)))
        return tuple(map(lambda a: a.encode('utf8'), l))
