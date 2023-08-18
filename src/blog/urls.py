""" URLs for the blog app """

from django.conf.urls import url

from . import views

__author__ = 'Alamgir Kabir Roni, Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# URLs
urlpatterns = [
    url(
        r'^$',
        views.blog_list,
        name='blog_list'
    ),
    url(
        r'^(?P<slug>[\w-]+)/$',
        views.blog_detail,
        name='blog_detail'
    ),
]
