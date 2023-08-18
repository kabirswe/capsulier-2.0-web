""" Models for the userprofile app """

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Models
class SignUp(models.Model):

    # Choices
    GENDER_CHOICE = [
        ('f', _('Mme')),
        ('m', _('M')),
    ]
    STATUS_CHOICE = [
        ('a', _('Public')),
        ('b', _('Professional')),
    ]

    # Relations
    user = models.OneToOneField(
        User,
        related_name='profile'
    )

    # Attributes
    company_name = models.CharField(
        _('company name'),
        max_length=80,
        blank=True,
    )
    date_of_birth = models.DateField(
        _('Date of birth'),
        blank=True,
        null=True,
    )
    gender = models.CharField(
        _('gender'),
        max_length=1,
        choices=GENDER_CHOICE,
        blank=True,
    )
    siret_number = models.CharField(
        _('siret number'),
        max_length=80,
        blank=True,
    )
    status = models.CharField(
        _('status'),
        max_length=1,
        choices=STATUS_CHOICE,
    )

    # Meta Data
    updated_on = models.DateTimeField(
        _('updated_on'),
        auto_now=True,
        auto_now_add=False,
    )
    created_on = models.DateTimeField(
        _('created_on'),
        auto_now=False,
        auto_now_add=True,
    )

    # Functions
    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    def __unicode__(self):
        return u"%s %s" % (self.user.first_name, self.user.last_name)

    # Meta
    class Meta:
        ordering = ['user']
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')
