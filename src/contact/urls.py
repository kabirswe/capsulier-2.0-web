""" URLs for the contact app """

from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

__author__ = 'Sathi'
__copyright__ = 'Copyright 2018, Maison Mahdil'


urlpatterns = [

    # Forms
    url(
        r'^contactform/$',
        views.contact_form,
        name='contactform'
    ),
    url(
        r'^newsletter/$',
        views.newsletter_form,
        name='newsletter'
    ),

    # Email
    url(
        r'^confirmation_mail/$',
        TemplateView.as_view(
            template_name='contact/email/confirmation_mail.html'
        )
    ),
    url(
        r'^customer_confirmation_mail/$',
        TemplateView.as_view(
            template_name='contact/email/customer_confirmation_mail.html'
        )
    ),
]
