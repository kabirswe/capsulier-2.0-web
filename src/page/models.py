""" Models for the page app """

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.utils.html import mark_safe
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.exceptions import InvalidImageFormatError
from geoposition.fields import GeopositionField
from image_cropping.fields import ImageRatioField
from phonenumber_field.modelfields import PhoneNumberField

from main.helpers import ActiveManager

from . import utils

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Models
class FAQ(models.Model):

    # Attributes
    content = models.TextField(
        _('content'),
        blank=True,
    )
    ordering = models.PositiveIntegerField(
        blank=False,
        default=0,
        null=False
    )
    title = models.CharField(
        _('title'),
        max_length=120
    )

    # Meta Data
    created_on = models.DateTimeField(
        _('created on'),
        auto_now_add=True,
        editable=False,
        null=True,
    )
    updated_on = models.DateTimeField(
        _('updated on'),
        auto_now=True,
        editable=False,
        null=True,
    )

    # Meta
    class Meta:
        ordering = ['ordering']
        verbose_name = _('faq')
        verbose_name_plural = _('faq')

    # Functions
    def __str__(self):
        return "%s" % (self.title)

    def __unicode__(self):
        return u"%s" % (self.title)

    # Others
    @staticmethod
    def get_last_index():
        obj = FAQ.objects.order_by('-ordering')[0]
        return obj.position

    # Save
    def save(self, *args, **kwargs):
        if self.ordering == 0:
            self.ordering = FAQ.get_last_index()
        return super(FAQ, self).save(*args, **kwargs)


class Partner(models.Model):

    # Manager
    objects = ActiveManager()

    # Relations
    sites = models.ManyToManyField(
        Site,
        verbose_name=_('sites'),
    )

    # Attributes
    active = models.BooleanField(
        _('active'),
        default=True,
    )
    category = models.CharField(
        _('category'),
        max_length=200,
        blank=True,
    )
    description = models.TextField(
        _('description'),
        blank=True,
    )
    index = models.PositiveIntegerField(
        blank=False,
        default=0,
        null=False,
    )
    image = models.ImageField(
        _('image'),
        upload_to=utils.page_upload_to,
    )
    image_cropping = ImageRatioField(
        'image',
        free_crop=True,
    )
    name = models.CharField(
        _('name'),
        max_length=200,
        blank=True,
    )
    slug = models.SlugField(
        _('slug'),
        editable=False,
    )
    link = models.URLField(
        _('link'),
        blank=True,
    )

    # Meta Data
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
    def __str__(self):
        return "%s" % (self.name)

    def __unicode__(self):
        return u"%s" % (self.name)

    def save(self, *args, **kwargs):
        super(Partner, self).save(*args, **kwargs)
        if self.index == 0:
            self.index = self.id
        self.slug = slugify(self.name)
        return super(Partner, self).save(*args, **kwargs)

    def get_image_box(self):
        if self.image:
            img = get_thumbnailer(self.image).get_thumbnail({
                'size': (400, 0),
                'box': self.image_cropping,
                'detail': True,
            }).url
            return mark_safe('<img src="%s" height="100" />' % img)
        else:
            return "%s" % (_('None'))
    get_image_box.short_description = _('Image')

    def get_image_hq(self):
        if self.image:
            try:
                return get_thumbnailer(self.image).get_thumbnail({
                    'size': (1600, 0),
                    'box': self.image_cropping,
                    'detail': True,
                }).url
            except InvalidImageFormatError:
                pass
        else:
            pass

    # Meta
    class Meta:
        ordering = ['index']
        verbose_name = _('Partner')
        verbose_name_plural = _('Partners')


class Schedule(models.Model):

    # Choices
    DAY_CHOICES = (
        ('1', _('Monday')),
        ('2', _('Tuesday')),
        ('3', _('Wednesday')),
        ('4', _('Thursday')),
        ('5', _('Friday')),
        ('6', _('Saturday')),
        ('7', _('Sunday')),
    )

    # Relations
    shop = models.ForeignKey(
        'Shop',
        verbose_name=_('shop'),
    )

    # Attributes
    afternoon_end_time = models.TimeField(
        _('afternoon end time'),
        blank=True,
        null=True,
    )
    afternoon_start_time = models.TimeField(
        _('afternoon start time'),
        blank=True,
        null=True,
    )
    close = models.BooleanField(
        _('close'),
        default=False
    )
    day = models.CharField(
        _('day'),
        choices=DAY_CHOICES,
        max_length=2,
    )
    morning_end_time = models.TimeField(
        _('morning end time'),
        blank=True,
        null=True,
    )
    morning_start_time = models.TimeField(
        _('morning start time'),
        blank=True,
        null=True,
    )

    # Meta Data
    created_on = models.DateTimeField(
        _('created on'),
        auto_now_add=True,
        blank=True,
        editable=False,
        null=True,
    )
    updated_on = models.DateTimeField(
        _('updated on'),
        auto_now=True,
        editable=False,
        null=True,
    )

    # Meta
    class Meta:
        unique_together = ('shop', 'day',)
        verbose_name = _('schedule')
        verbose_name_plural = _('schedules')

    # Functions
    def __str__(self):
        return "%s - %s" % (self.shop, self.day)

    def __unicode__(self):
        return u"%s - %s" % (self.shop, self.day)


class Shop(models.Model):

    # Relations
    sites = models.ManyToManyField(
        Site,
        verbose_name=_('sites'),
    )

    # Attributes
    active = models.BooleanField(
        _('active'),
        default=True
    )
    address = GeopositionField(
        _('address'),
    )
    address2 = models.CharField(
        _('address2'),
        blank=True,
        max_length=180,
    )
    email = models.EmailField(
        _('e-mail'),
        blank=True,
    )
    image = models.ImageField(
        _('image'),
        upload_to=utils.page_upload_to,
        help_text=_('At least 800px wide'),
    )
    image_cropping = ImageRatioField(
        'image',
        free_crop=True,
    )
    logo = models.FileField(
        blank=True,
        upload_to=utils.page_upload_to,
    )
    name = models.CharField(
        _('name'),
        blank=True,
        max_length=200,
        unique=True,
    )
    phone = PhoneNumberField(
        _('phone number'),
        blank=True,
    )
    slug = models.SlugField(
        _('slug'),
        editable=False,
        unique=True,
    )
    website = models.URLField(
        _('website'),
        blank=True,
    )

    # Meta Data
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

    # Meta
    class Meta:
        ordering = ['name']
        verbose_name = _('shop')
        verbose_name_plural = _('shops')

    # Functions
    def __str__(self):
        return "%s" % (self.name)

    def __unicode__(self):
        return u"%s" % (self.name)

    def get_image_mq(self):
        if self.image:
            try:
                return get_thumbnailer(self.image).get_thumbnail({
                    'size': (800, 0),
                    'box': self.image_cropping,
                    'detail': True,
                }).url
            except InvalidImageFormatError:
                pass

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Shop, self).save(*args, **kwargs)


class Slider(models.Model):

    # Relations
    sites = models.ManyToManyField(
        Site,
        verbose_name=_('sites'),
    )

    # Attributes
    button_text = models.CharField(
        _('button text'),
        max_length=200,
        blank=True,
    )
    index = models.PositiveIntegerField(
        blank=False,
        default=0,
        null=False,
    )
    image = models.ImageField(
        _('image'),
        upload_to=utils.page_upload_to,
    )
    image_cropping = ImageRatioField(
        'image',
        '1600x1067',
    )
    title = models.CharField(
        _('alt tag'),
        blank=True,
        max_length=200,
    )
    slug = models.SlugField(
        _('slug'),
        blank=True,
        null=True,
        unique=False,
    )
    url = models.URLField(
        _('url'),
        blank=True,
    )

    # Meta Data
    created_on = models.DateTimeField(
        _('created on'),
        auto_now_add=True,
        editable=False,
        null=True,
    )
    created_by = models.ForeignKey(
        User,
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

    # Meta
    class Meta:
        ordering = ['-index']
        verbose_name = _('Slider')
        verbose_name_plural = _('Slider')

    # Functions
    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    @staticmethod
    def get_last_index():
        try:
            obj = Slider.objects.order_by('-index')[0]
            return obj.index
        except IndexError:
            return 0

    def get_image_box(self):
        if self.image:
            try:
                img = get_thumbnailer(self.image).get_thumbnail({
                    'size': (400, 0),
                    'box': self.image_cropping,
                    'detail': True,
                }).url
                return mark_safe('<img src="%s" height="100" />' % img)
            except InvalidImageFormatError:
                pass
        else:
            return "%s" % (_('None'))
    get_image_box.short_description = _('Image')

    def get_image_hq(self):
        if self.image:
            try:
                return get_thumbnailer(self.image).get_thumbnail({
                    'size': (1600, 0),
                    'box': self.image_cropping,
                    'detail': True,
                }).url
            except InvalidImageFormatError:
                pass
        else:
            pass

    def save(self, *args, **kwargs):
        if self.index == 0:
            self.index = Slider.get_last_index() + 1
        self.slug = slugify(self.title)
        return super(Slider, self).save(*args, **kwargs)


class TeamMember(models.Model):

    # Relations
    shop = models.ForeignKey(
        Shop,
        verbose_name=_('shop'),
    )

    # Attributes
    first_name = models.CharField(
        _('first name'),
        max_length=200,
    )
    image = models.ImageField(
        _('image'),
        upload_to=utils.page_upload_to,
    )
    image_cropping = ImageRatioField(
        'image',
        '1200x1800',
    )
    last_name = models.CharField(
        _('last name'),
        max_length=200,
    )
    slug = models.SlugField(
        _('slug'),
        editable=False,
    )

    # Metadata
    created_on = models.DateTimeField(
        _('created on'),
        auto_now_add=True,
        blank=True,
        editable=False,
        null=True,
    )
    updated_on = models.DateTimeField(
        _('updated on'),
        auto_now=True,
        editable=False,
        null=True,
    )

    # Meta
    class Meta:
        verbose_name = _('team member')
        verbose_name_plural = _('team members')

    # Functions
    def __str__(self):
        return "%s - %s" % (self.first_name, self.last_name)

    def __unicode__(self):
        return u"%s - %s" % (self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        self.slug = '-'.join([slugify(self.first_name), slugify(self.last_name)])
        return super(TeamMember, self).save(*args, **kwargs)


class ConceptMap(models.Model):
    # Attributes
    address = GeopositionField(
        _('address'),
    )
    marker = models.FileField(
        blank=True,
        upload_to=utils.marker_upload_to,
    )
    name = models.CharField(
        _('name'),
        blank=True,
        max_length=200,
        unique=True,
    )
    # Meta Data
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

    # Meta
    class Meta:
        ordering = ['name']
        verbose_name = _('concept map')
        verbose_name_plural = _('concept maps')

    # Functions
    def __str__(self):
        return "%s" % (self.name)

    def __unicode__(self):
        return u"%s" % (self.name)
