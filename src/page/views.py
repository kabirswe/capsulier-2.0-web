""" Views for the page app """

from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from blog import models as blog_models
from eshop import forms as eshop_forms
from eshop import models as eshop_models
from product import models as product_models
from main import utils as main_utils

from . import models
from . import serializers


__author__ = 'Sathi, Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Views
def cgv(request):
    seo = main_utils.get_seo(3)
    context = {
        'seo': seo,
    }
    return render(request, 'page/cgv.html', context)


def concept(request):
    seo = main_utils.get_seo(4)
    current_site = get_current_site(request)
    partners_list = models.Partner.objects.active().filter(sites=current_site)
    context = {
        'partners_list': partners_list,
        'seo': seo,
        'navbar': 'concept',
    }
    if current_site.id == 1:
        template_url = 'page/concept_capsulier.html'
    else:
        template_url = 'page/concept_conservatoire.html'
    return render(request, template_url, context)


def eshop(request):
    seo = main_utils.get_seo(5)
    current_site = get_current_site(request)
    if current_site.id == 2:
        product_list = product_models.Product.objects.active().filter(sites=2)
        context = {
            'product_list': product_list,
            'seo': seo,
        }
        return render(request, 'page/eshop.html', context)
    else:
        raise Http404


def faq(request):
    seo = main_utils.get_seo(14)
    object_list = models.FAQ.objects.all()
    context = {
        'seo': seo,
        'object_list': object_list,
    }
    return render(request, 'page/faq.html', context)


def home(request):
    seo = main_utils.get_seo(1)
    current_site = get_current_site(request)
    slider_list = models.Slider.objects.filter(sites=current_site)
    blog_list = blog_models.Post.objects.active().filter(sites=current_site)
    category_list = product_models.Category.objects.active().exclude(id=1)
    capsule_list = product_models.Product.objects.active().filter(category__id=1).order_by('?')
    other_list = product_models.Product.objects.active().exclude(
        category__id=1).filter(sites=current_site).order_by('?')[:5]
    context = {
        'page': 'home',
        'blog_list': blog_list,
        'category_list': category_list,
        'capsule_list': capsule_list,
        'other_list': other_list,
        'slider_list': slider_list,
        'seo': seo,
    }
    if current_site.id == 1:
        template_url = 'page/home_capsulier.html'
    else:
        template_url = 'page/home_conservatoire.html'
    return render(request, template_url, context)


def legal_notice(request):
    seo = main_utils.get_seo(6)
    context = {
        'seo': seo,
    }
    return render(request, 'page/legal_notice.html', context)


def map(request):
    seo = main_utils.get_seo(7)
    current_site = get_current_site(request)
    if current_site.id == 2:
        context = {
            'seo': seo,
        }
        return render(request, 'page/map.html', context)
    else:
        raise Http404


def pro(request):
    return render(request, 'page/pro.html', {})


def shop(request):
    seo = main_utils.get_seo(8)
    instance = models.Shop.objects.get(id=1)
    object_list = models.Shop.objects.all()
    context = {
        'instance': instance,
        'object_list': object_list,
        'seo': seo,
        'navbar': 'boutiques',
    }
    return render(request, 'page/shop.html', context)


# To check
class ShopAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = models.Shop.objects.all()
    serializer_class = serializers.ShopSerializers


def address_edit(request, id):
    address_instance = get_object_or_404(eshop_models.UserAddress, id=id)
    if request.method == 'POST':
        form = eshop_forms.UserAddressForm(request.POST, instance=address_instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect('userprofile:profile')
    else:
        form = eshop_forms.UserAddressForm(instance=address_instance)
    return render(request, 'page/address_edit.html', {'form': form})
