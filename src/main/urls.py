""" URLs for the main app """

from django.conf.urls import url
from django.views.generic import TemplateView

__author__ = 'Sathi'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Errors pages
urlpatterns = [
    url(
        r'^error/400/$',
        TemplateView.as_view(template_name='main/error/400.html')
    ),
    url(
        r'^error/403/$',
        TemplateView.as_view(template_name='main/error/403.html')
    ),
    url(
        r'^error/403_csrf/$',
        TemplateView.as_view(template_name='main/error/403_csrf.html')
    ),
    url(
        r'^error/404/$',
        TemplateView.as_view(template_name='main/error/404.html')
    ),
    url(
        r'^error/500/$',
        TemplateView.as_view(template_name='main/error/500.html')
    ),
    url(
        r'^account/email_confirmation_message/$',
        TemplateView.as_view(template_name='account/email/email_confirmation_message.html')
    ),
    url(
        r'^account/email_confirmation_signup_message/$',
        TemplateView.as_view(template_name='account/email/email_confirmation_signup_message.html')
    ),
    url(
        r'^account/password_reset_key_message/$',
        TemplateView.as_view(template_name='account/email/password_reset_key_message.html')
    ),
]
