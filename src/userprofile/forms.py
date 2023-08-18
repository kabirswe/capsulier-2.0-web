""" Forms for the userprofile app """

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from . import models

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Forms
class SignupFormEdit(forms.ModelForm):

    class Meta:
        model = models.SignUp
        fields = [
            'gender',
            'date_of_birth',
            'company_name',
            'siret_number',
        ]


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]


class SignupForm(forms.ModelForm):

    # Choices
    GENDER_CHOICE = [
        ('f', _('Mme')),
        ('m', _('M')),
    ]
    STATUS_CHOICE = [
        ('a', _('Private')),
        ('b', _('Professional')),
    ]

    # Fields
    # company_name = forms.CharField(
    #     max_length=40,
    #     label=_('Company name'),
    # )
    # date_of_birth = forms.DateField(
    #     label=_('Date of Birth'),
    #     widget=forms.TextInput(attrs={'placeholder': _('Date of Birth')})
    # )
    first_name = forms.CharField(
        max_length=40,
        label=_('First name'),
    )
    gender = forms.ChoiceField(
        label=_('Gender'),
        choices=GENDER_CHOICE,
        widget=forms.RadioSelect()
    )
    last_name = forms.CharField(
        max_length=40,
        label=_('Last name'),
    )
    # siret_number = forms.CharField(
    #     max_length=40,
    #     label=_('Siret number'),
    # )
    status = forms.ChoiceField(
        label=_('Status'),
        choices=STATUS_CHOICE,
        widget=forms.RadioSelect()
    )

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

    def signup(self, request, user):
        UserData = models.SignUp()
        UserData.user = user
        UserData.gender = self.cleaned_data['gender']
        UserData.status = self.cleaned_data['status']
        if self.cleaned_data['status'] == 'b':
            UserData.company_name = self.cleaned_data['company_name']
            UserData.siret_number = self.cleaned_data['siret_number']
        UserData.save()

    class Meta:
        model = models.SignUp
        fields = (
            # 'date_of_birth',
            'gender',
            'status',
            'company_name',
            'siret_number',

        )
