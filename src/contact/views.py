""" Views for the contact app """

import json
import mailchimp

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from main.models import Text

from . import forms

__author__ = 'Sathi'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Views
def contact_form(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            text_list = Text.objects.all()
            instance.save()
            ctx = {
                'instance': instance,
                'text_list': text_list,
            }
            msg_plain = render_to_string(
                'contact/email/confirmation_mail.txt',
                ctx
            )
            msg_html = render_to_string(
                'contact/email/confirmation_mail.html',
                ctx
            )
            subject = _('Subject')
            message = msg_plain
            from_email = settings.EMAIL_HOST_USER
            to_list = [settings.ADMIN]
            send_mail(
                subject,
                message,
                from_email,
                to_list,
                html_message=msg_html,
                fail_silently=True
            )
            customer_msg_plain = render_to_string(
                'contact/email/customer_confirmation_mail.txt',
                ctx
            )
            customer_msg_html = render_to_string(
                'contact/email/customer_confirmation_mail.html',
                ctx
            )
            subject = _('Subject')
            message = customer_msg_plain
            from_email = settings.EMAIL_HOST_USER
            to_list = [request.user.email]
            send_mail(
                subject,
                message,
                from_email,
                to_list,
                html_message=customer_msg_html,
                fail_silently=True
            )
            ajaxData = {}
            ajaxData['success_msg'] = ('Success message')
            return HttpResponse(json.dumps(ajaxData))
        else:
            ajaxData = {}
            ajaxData['error_msg'] = ('Error message')
            return HttpResponse(json.dumps(ajaxData))
    else:
        form = forms.ContactForm()

    context = {
        'form': form,
    }
    return render(request, 'contact/contact_form.html', context)


def newsletter_form(request):
    current_site = get_current_site(request)
    if settings.MAILCHIMP_LIST_ID:
        list_id = settings.MAILCHIMP_LIST_ID
        instance = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)
    else:
        list_id = current_site.siteextra.mailchimp_list_id
        instance = mailchimp.Mailchimp(current_site.siteextra.mailchimp_api_key)
    if request.method == 'POST':
        form = forms.NewsletterForm(request.POST or None)
        if form.is_valid():
            email = {"email": form.cleaned_data.get("email_address")}
            instance.lists.subscribe(
                list_id, email,
                double_optin=False,
                update_existing=True,
                send_welcome=False
            )
            ajaxData = {}
            ajaxData['success_msg'] = 'Success Newsletter message'
            return HttpResponse(json.dumps(ajaxData))
        else:
            ajaxData = {}
            ajaxData['error_msg'] = 'Error Newsletter message'
            return HttpResponse(json.dumps(ajaxData))
    else:
        form = forms.NewsletterForm()

    context = {
        'newsletter_form': form,
    }
    return render(request, 'contact/newsletter_form.html', context)
