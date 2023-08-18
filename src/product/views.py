""" Views for the product app """

from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.shortcuts import render, get_object_or_404

from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from itertools import chain

from main import utils as main_utils

from . import models
from . import serializers

__author__ = 'S. M. Sazedul Haque, Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Views
def category_detail(request, slug=None):
    current_site = get_current_site(request)
    if current_site.id == 2:
        instance = get_object_or_404(models.Category, slug=slug)
        product_object_list = models.Product.objects.filter(
            category=instance, sites=current_site
        )
        seo = instance
        context = {
            'instance': instance,
            'product_list': product_object_list,
            'seo': seo,
        }
        return render(request, 'product/product_list_conservatoire.html', context)
    else:
        raise Http404


def product_list(request):
    seo = main_utils.get_seo(9)
    current_site = get_current_site(request)
    product_object_list = models.Product.objects.active().filter(sites=current_site)
    context = {
        'product_list': product_object_list,
        'navbar': 'product',
        'seo': seo,
    }
    if current_site.id == 1:
        template_url = 'product/product_list_capsulier.html'
    else:
        template_url = 'product/product_list_conservatoire.html'
    return render(request, template_url, context)


def product_detail(request, slug=None):
    current_site = get_current_site(request)
    instance = get_object_or_404(models.Product, slug=slug)
    seo = instance
    if current_site.id == 1:
        product_list1 = models.Product.objects.active().filter(
            category__id=1).filter(sites=1).exclude(slug=slug).order_by('?')
        product_list2 = models.Product.objects.filter(slug=slug)
        product_object_list = list(chain(product_list2, product_list1))
        other_list = models.Product.objects.active().filter(
            sites=1).exclude(slug=slug).order_by('?')[:4]
        if instance.category.id == 1:
            template_url = 'product/product_detail_capsulier.html'
        else:
            template_url = 'product/product_detail_capsulier_others.html'
    else:
        product_list1 = ''
        product_object_list = models.Product.objects.filter(
            sites=2
        ).exclude(slug=slug).order_by('?')[:4]
        other_list = models.Product.objects.active().filter(
            sites=2).exclude(slug=slug).order_by('?')[:4]
        template_url = 'product/product_detail_capsulier_others.html'
    context = {
        'instance': instance,
        'product_list': product_object_list,
        'product_list1': product_list1,
        'other_list': other_list,
        'seo': seo,
    }
    return render(request, template_url, context)


# API
class ProductAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = models.Product.objects.map().filter(sites=2)
    serializer_class = serializers.ProductSerializers
