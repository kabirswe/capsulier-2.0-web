""" Forms for the contact app """

from django import forms

from . import models

__author__ = 'Sathi, Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Forms
class ContactForm(forms.ModelForm):
    class Meta:
        model = models.Contact

        fields = [
            'name',
            'email',
            'message',
        ]


class NewsletterForm(forms.Form):
    email_address = forms.EmailField()
