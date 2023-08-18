# pylint: disable=no-member
# pylint: disable=C0111

""" Views for the userprofile app """

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

from eshop.models import Order, UserAddress
from main import models as main_models

from . import forms
from . import models

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Views
@login_required
def profile(request):
    try:
        seo = main_models.SEO.objects.get(id=10)
    except ObjectDoesNotExist:
        seo = main_models.SEO.objects.get(id=1)
    except ObjectDoesNotExist:
        seo = None
    address_billing_object_list = UserAddress.objects.filter(
        Q(types='a') | Q(types='b'),
        user__user=request.user
    )
    address_shipping_object_list = UserAddress.objects.filter(
        Q(types='a') | Q(types='s'),
        user__user=request.user
    )
    order_object_list = Order.objects.filter(user_checkout__user=request.user).exclude(status='c')
    profile_instance = models.SignUp.objects.get(user=request.user)
    if request.method == 'POST':
        form = forms.SignupFormEdit(
            request.POST or None,
            request.FILES or None,
            instance=profile_instance
        )
        form2 = forms.UserForm(
            request.POST or None,
            request.FILES or None,
            instance=request.user
        )
        if form.is_valid() and form2.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            instance2 = form2.save(commit=False)
            instance2.save()
            return HttpResponseRedirect(reverse('userprofile:profile'))
    else:
        form = forms.SignupFormEdit(instance=profile_instance)
        form2 = forms.UserForm(instance=request.user)
    context = {
        'address_billing_object_list': address_billing_object_list,
        'address_shipping_object_list': address_shipping_object_list,
        'order_object_list': order_object_list,
        'form': form,
        'form2': form2,
        'instance': profile_instance,
        'seo': seo,
    }
    return render(request, 'userprofile/profile.html', context)
