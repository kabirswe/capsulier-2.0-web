""" Views for the blog app """

from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, get_object_or_404

from main import utils as main_utils

from . import models

__author__ = 'Alamgir Kabir Roni, Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Views
def blog_detail(request, slug=None):
    current_site = get_current_site(request)
    instance = get_object_or_404(models.Post, slug=slug, sites=current_site)
    blog_object_list = models.Post.objects.all().exclude(slug=slug)
    seo = instance
    context = {
        'instance': instance,
        'blog_list': blog_object_list,
        'seo': seo,
        'navbar': 'blog',
    }
    return render(request, 'blog/blog_detail.html', context)


def blog_list(request):
    seo = main_utils.get_seo(2)
    current_site = get_current_site(request)
    object_list = models.Post.objects.active().filter(sites=current_site)
    context = {
        'object_list': object_list,
        'seo': seo,
        'navbar': 'blog',
    }
    return render(request, 'blog/blog_list.html', context)
