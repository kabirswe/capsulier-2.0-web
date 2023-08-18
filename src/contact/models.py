""" Models for the contact app """

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


# Models
class Contact(models.Model):

    # Attributes
    name = models.CharField(
        _('name'),
        max_length=120,
    )
    email = models.EmailField(
        _('email'),
    )
    message = models.TextField(
        _('message'),
    )

    # Meta Data
    created_on = models.DateTimeField(
        _('created on'),
        auto_now_add=True,
        editable=False,
        null=True,
    )

    # Functions
    def __str__(self):
        return "%s" % (self.name)

    def __unicode__(self):
        return u"%s" % (self.name)

    # Meta
    class Meta:
        ordering = ['-created_on']
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')
