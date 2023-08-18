""" mahdil URL Configuration """

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from mahdil.sitemaps import main_sitemaps

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# URLs
urlpatterns = i18n_patterns(

    # Admin
    url(
        r'^admin/',
        include(admin.site.urls)
    ),

    # Third party apps URLs
    url(
        r'^accounts/',
        include('allauth.urls')
    ),
    url(
        r'^ckeditor/',
        include('ckeditor_uploader.urls')
    ),

    # Pages
    url(
        r'^',
        include('page.urls', namespace='page')
    ),
    url(
        r'^blog/',
        include('blog.urls', namespace='blog')
    ),
    url(
        r'^contact/',
        include('contact.urls', namespace='contact')
    ),
    url(
        r'^eshop/',  # Linked to external payment module
        include('eshop.urls', namespace='eshop')
    ),
    url(
        r'^my-caps/',
        include('mycaps.urls', namespace='mycaps')
    ),
    url(
        r'^capsule-compatible-nespresso/',
        include('product.urls', namespace='product')
    ),
    url(
        r'^produits/',
        include('product.urls', namespace='product-others')
    ),
    url(
        r'^profil/',
        include('userprofile.urls', namespace='userprofile')
    ),
    url(
        r'^main/',
        include('main.urls', namespace='main')
    ),

    # API
    url(
        r'^api/main/',
        include('main.api.urls', namespace='main_api')
    ),
    url(
        r'^api/product/',
        include('product.api.urls', namespace='product_api')
    ),
    url(
        r'^api/page/',
        include('page.api.urls', namespace='page_api')
    ),

    # Sitemap,
    url(
        r'^sitemap\.xml$',
        sitemap, {'sitemaps': main_sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),
)

urlpatterns += [

    # Robots,
    url(
        r'^robots\.txt$',
        TemplateView.as_view(template_name='main/robots.txt')
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
