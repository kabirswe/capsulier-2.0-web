""" Models for the mycaps app """

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from easy_thumbnails.exceptions import InvalidImageFormatError
from easy_thumbnails.files import get_thumbnailer

from product.models import Product

from . import utils

__author__ = 'Aupourbau Koumar, Alamgir Kabir Roni'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Models
class Coffee(models.Model):

    # Attributes
    title = models.CharField(
        _('title'),
        max_length=200,
        unique=True,
    )
    description = models.TextField(
        _('description'),
        blank=True,
    )
    image = models.FileField(
        _('image'),
        blank=True,
        upload_to=utils.mycaps_upload_to,
    )

    # Metadata
    created_on = models.DateTimeField(
        _('created on'),
        auto_now_add=True,
        blank=True,
        editable=False,
        null=True,
    )
    created_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name='+',
        verbose_name=_('created by'),
    )
    updated_on = models.DateTimeField(
        _('updated on'),
        auto_now=True,
        editable=False,
        null=True,
    )
    updated_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name='+',
        verbose_name=_('updated by'),
    )

    # Functions
    def __unicode__(self):
        return self.title

    def __unicode__(self):
        return u"%s" % (self.title)

    def get_image_box(self):
        if self.image:
            try:
                img = self.image.url
                return mark_safe('<img src="%s" width="120px" />' % img)
            except InvalidImageFormatError:
                return "%s" % (_('Image File Error'))
        else:
            return "%s" % (_('None'))
    get_image_box.short_description = _('Coffee Image')


class Color(models.Model):

    # Attributes
    name = models.CharField(
        _('name'),
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        _('color'),
        max_length=200,
    )
    image = models.ImageField(
        _('image'),
        blank=False,
        upload_to=utils.mycaps_upload_to,
    )
    color_image = models.ImageField(
        _('color image'),
        blank=True,
        upload_to=utils.mycaps_upload_to,
    )
    package_image = models.ImageField(
        _('package image'),
        blank=True,
        upload_to=utils.mycaps_upload_to,
    )
    background_image = models.ImageField(
        _('background image'),
        blank=True,
        upload_to=utils.mycaps_upload_to,
    )

    # Metadata
    created_on = models.DateTimeField(
        _('created on'),
        auto_now_add=True,
        blank=True,
        editable=False,
        null=True,
    )
    created_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name='+',
        verbose_name=_('created by'),
    )
    updated_on = models.DateTimeField(
        _('updated on'),
        auto_now=True,
        editable=False,
        null=True,
    )
    updated_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name='+',
        verbose_name=_('updated by'),
    )

    # Functions
    def __unicode__(self):
        return self.name

    def __unicode__(self):
        return u"%s" % (self.name)

    def get_image_box(self):
        if self.image:
            try:
                img = get_thumbnailer(self.image).get_thumbnail({
                    'size': (400, 0),
                    'detail': True,
                }).url
                return mark_safe('<img src="%s" width="80px" />' % img)
            except InvalidImageFormatError:
                return "%s" % (_('Image File Error'))
        else:
            return "%s" % (_('None'))
    get_image_box.short_description = _('Image')

    def get_image_box_color(self):
        if self.color_image:
            try:
                img = get_thumbnailer(self.color_image).get_thumbnail({
                    'size': (400, 0),
                    'detail': True,
                }).url
                return mark_safe('<img src="%s" width="120px" />' % img)
            except InvalidImageFormatError:
                return "%s" % (_('Image File Error'))
        else:
            return "%s" % (_('None'))
    get_image_box_color.short_description = _('Color Image')

    def get_image_box_package(self):
        if self.package_image:
            try:
                img = get_thumbnailer(self.package_image).get_thumbnail({
                    'size': (400, 0),
                    'detail': True,
                }).url
                return mark_safe('<img src="%s" width="120px" />' % img)
            except InvalidImageFormatError:
                return "%s" % (_('Image File Error'))
        else:
            return "%s" % (_('None'))
    get_image_box_package.short_description = _('Package Image')

    def get_image_box_background(self):
        if self.background_image:
            try:
                img = get_thumbnailer(self.background_image).get_thumbnail({
                    'size': (400, 0),
                    'detail': True,
                }).url
                return mark_safe('<img src="%s" width="120px" />' % img)
            except InvalidImageFormatError:
                return "%s" % (_('Image File Error'))
        else:
            return "%s" % (_('None'))
    get_image_box_background.short_description = _('Background Image')


class Package(models.Model):

    # Relations
    coffee = models.ForeignKey(
        Coffee,
        verbose_name=_('coffee'),
        related_name='packagebycoffee',
    )
    color = models.ForeignKey(
        Color,
        verbose_name=_('color'),
        related_name='packagebycolor',
    )
    product = models.ForeignKey(
        Product,
        verbose_name=_('product'),
        related_name='packagebyproduct',
        default='310',
    )

    # Attributes
    image = models.ImageField(
        _('image'),
        blank=True,
        upload_to=utils.mycaps_upload_to,
    )
    image1 = models.ImageField(
        _('image1'),
        blank=True,
        upload_to=utils.mycaps_upload_to,
    )
    text1 = models.CharField(
        _('text for capsule'),
        max_length=200,
        blank=True,
    )
    text2 = models.CharField(
        _('text for package'),
        max_length=200,
        blank=True,
    )
    active = models.BooleanField(
        _('active'),
        default=True,
    )

    # Metadata
    created_on = models.DateTimeField(
        _('created on'),
        auto_now_add=True,
        editable=False,
    )
    updated_on = models.DateTimeField(
        _('updated on'),
        auto_now=True,
        editable=False,
        null=True,
    )

    # Functions
    def __unicode__(self):
        return self.id

    def __unicode__(self):
        return u"%s" % (self.id)

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    def get_image_box(self):
        if self.image:
            try:
                img = get_thumbnailer(self.image).get_thumbnail({
                    'size': (400, 0),
                    'detail': True,
                }).url
                return mark_safe('<img src="%s" width="200px" />' % img)
            except InvalidImageFormatError:
                return "%s" % (_('Image File Error'))
        else:
            return "%s" % (_('None'))
    get_image_box.short_description = _('Image')

    def get_image_box2(self):
        if self.image1:
            try:
                img = get_thumbnailer(self.image1).get_thumbnail({
                    'size': (400, 0),
                    'detail': True,
                }).url
                return mark_safe('<img src="%s" width="200px" />' % img)
            except InvalidImageFormatError:
                return "%s" % (_('Image File Error'))
        else:
            return "%s" % (_('None'))
    get_image_box.short_description = _('Image2')

    def add_to_cart(self):
        return "%s?package=%s&qty=1" % (reverse('eshop:cart'), self.id)

    def remove_from_cart(self):
        return "%s?package=%s&qty=1&delete=True" % (reverse('eshop:cart'), self.id)

    def get_title(self):
        return "%s - %s" % (self.product.name, self.title)
    # Meta

    class Meta:
        ordering = ['id']
        verbose_name = _('package')
        verbose_name_plural = _('packages')


class Crop(models.Model):
    image = models.ImageField(
        _('image'),
        blank=True,
        upload_to=utils.mycaps_upload_to,
    )

    # Metadata
    created_on = models.DateTimeField(
        _('created on'),
        auto_now_add=True,
        editable=False,
    )
    updated_on = models.DateTimeField(
        _('updated on'),
        auto_now=True,
        editable=False,
        null=True,
    )

    class Meta:
        ordering = ['id']
        verbose_name = _('crop')
        verbose_name_plural = _('cropes')
