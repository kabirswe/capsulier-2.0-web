""" mahdil sitemaps Configuration """

from django.contrib.sitemaps import Sitemap, GenericSitemap
from django.core.urlresolvers import reverse

from datetime import datetime

from blog import models as blog_models
from product import models as product_models

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Sitemaps
class StaticSitemap(Sitemap):
    priority = 0.9

    def __init__(self, names):
        self.names = names

    def items(self):
        return self.names

    def changefreq(self, obj):
        return 'weekly'

    def lastmod(self, obj):
        return datetime.now()

    def location(self, obj):
        return reverse(obj)


# URLs
blog_dict = {
    'queryset': blog_models.Post.objects.active(),
    'date_field': 'updated_on',
}
category_dict = {
    'queryset': product_models.Category.objects.active(),
    'date_field': 'updated_on',
}
product_dict = {
    'queryset': product_models.Product.objects.active(),
    'date_field': 'updated_on',
}

main_sitemaps = {
    'site': StaticSitemap([
        'page:home',
    ]),
    'blog_object': GenericSitemap(blog_dict, priority=0.8),
    'category_object': GenericSitemap(category_dict, priority=0.8),
    'product_object': GenericSitemap(product_dict, priority=0.8),
}
