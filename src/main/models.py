""" Models for the main app """

from __future__ import unicode_literals

import uuid

from django.contrib.sites.models import Site
from django.db import models
from django.utils import timezone
from django.utils.html import mark_safe
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from ckeditor.fields import RichTextField
from easy_thumbnails.exceptions import InvalidImageFormatError
from easy_thumbnails.files import get_thumbnailer
from image_cropping import ImageRatioField
from geoposition.fields import GeopositionField

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Functions
def file_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return "main/%s/%s" % (
        timezone.now().strftime('%Y/%m/%d'),
        filename
    )


# Models
class Page(models.Model):

    # Attributes
    html = models.CharField(
        _('html'),
        blank=True,
        max_length=80,
    )
    name = models.CharField(
        _('name'),
        max_length=80,
    )
    slug = models.SlugField(
        _('slug'),
        unique=True,
        max_length=206,
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
        ordering = ['name']
        verbose_name = _('Static Page')
        verbose_name_plural = _('Static Pages')

    # Functions
    def __str__(self):
        return "%s" % (self.name)

    def __unicode__(self):
        return u"%s" % (self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Page, self).save(*args, **kwargs)

    def text_count(self):
        return Text.objects.filter(page=self).count()


class SEO(models.Model):

    # Relations
    page = models.ForeignKey(
        Page,
        verbose_name=_('page'),
    )

    # Attributes
    title = models.CharField(
        _('title'),
        help_text=_('The title of the page.'),
        max_length=60,
    )
    description = models.TextField(
        _('description'),
        blank=True,
        help_text=_('A short description or summary of the page. (max 160 characters)'),
        max_length=160,
    )
    keywords = models.TextField(
        _('keywords'),
        blank=True,
        help_text=_('A series of keywords you deem relevant to the page.'),
    )
    resource_type = models.CharField(
        'Resource-type',
        blank=True,
        help_text=_('Defines the type of webpage.'),
        max_length=120,
    )
    image = models.ImageField(
        _('image'),
        blank=True,
        help_text=_('It should be at least 600x315 pixels, but 1200x630 or larger is preferred (up to 5MB).'),
        upload_to=file_upload_to
    )
    image_cropping = ImageRatioField(
        'image',
        '1200x630',
    )
    fb_app_id = models.CharField(
        'fb:app_id',
        blank=True,
        max_length=60,
    )
    site_name = models.CharField(
        'og:site_name',
        blank=True,
        help_text=_('The name which should be displayed for the overall site.'),
        max_length=60,
    )
    twitter_site = models.CharField(
        'twitter:site',
        blank=True,
        help_text=_('@username of website.'),
        max_length=60,
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
        ordering = ['page']
        verbose_name = _('SEO')
        verbose_name_plural = _('SEO')

    # Functions
    def __str__(self):
        return "%s" % (self.page)

    def __unicode__(self):
        return u"%s" % (self.page)

    def get_image_box(self):
        if self.image:
            try:
                img = get_thumbnailer(self.image).get_thumbnail({
                    'size': (400, 0),
                    'box': self.image_cropping,
                    'detail': True,
                }).url
                return mark_safe(
                    '<img src="%s" height="100"/>'
                    % (img)
                )
            except InvalidImageFormatError:
                return "%s" % (_('Image File Error'))
        else:
            return "%s" % (_('None'))
    get_image_box.short_description = _('Image')

    def get_image_hq(self):
        if self.image:
            try:
                return get_thumbnailer(self.image).get_thumbnail({
                    'size': (1200, 0),
                    'box': self.image_cropping,
                    'detail': True,
                }).url
            except InvalidImageFormatError:
                pass
        else:
            pass

    # SEO
    def get_seo_description(self):
        if self.description:
            return self.description
        seo_main = SEO.objects.get(id=1)
        return seo_main.description

    def get_seo_image(self):
        if self.image:
            return self.get_image_hq()
        seo_main = SEO.objects.get(id=1)
        return seo_main.get_image_hq()

    def get_seo_title(self):
        return self.title


class SiteExtra(models.Model):

    # Relations
    site = models.OneToOneField(
        Site,
        verbose_name=_('site'),
    )

    # Attributes
    google_analytics_id = models.CharField(
        _('google analytics id'),
        blank=True,
        max_length=40,
    )
    mailchimp_api_key = models.CharField(
        _('mailchimp api key'),
        blank=True,
        max_length=40,
    )
    mailchimp_list_id = models.CharField(
        _('mailchimp list id'),
        blank=True,
        max_length=40,
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
        ordering = ['site']
        verbose_name = _('Site Extra')
        verbose_name_plural = _('Site Extra')

    # Functions
    def __str__(self):
        return "%s" % (self.site)

    def __unicode__(self):
        return u"%s" % (self.site)

    def get_site_id(self):
        return self.site.id

    def get_site_name(self):
        return self.site.name


class Text(models.Model):

    # Choices
    CROP_CHOICES = (
        ('f', _('free')),
        ('r', _('16x9 ratio')),
        ('s', _('square')),
    )

    # Relations
    page = models.ForeignKey(
        Page,
        verbose_name=_('page'),
    )

    # Attributes
    position = models.PositiveIntegerField(
        blank=False,
        default=0,
        null=False
    )
    t_CharField = models.CharField(
        'CharField',
        blank=True,
        max_length=120,
    )
    t_CharField_boolean = models.BooleanField(
        'CharField boolean',
        default=False,
    )
    t_CharField_slug = models.SlugField(
        'CharField slug',
        blank=True,
        max_length=120,
    )
    t_EmailField = models.EmailField(
        'EmailField',
        blank=True,
    )
    t_EmailField_boolean = models.BooleanField(
        'EmailField boolean',
        default=False,
    )
    t_FileField = models.FileField(
        'FileField',
        blank=True,
        upload_to=file_upload_to
    )
    t_FileField_boolean = models.BooleanField(
        'FileField boolean',
        default=False,
    )
    t_GeopositionField = GeopositionField(
        'GeopositionField',
        blank=True,
    )
    t_GeopositionField_boolean = models.BooleanField(
        'GeopositionField boolean',
        default=False,
    )
    t_ImageField = models.ImageField(
        'image',
        blank=True,
        upload_to=file_upload_to
    )
    t_ImageField_boolean = models.BooleanField(
        'ImageField boolean',
        default=False,
    )
    t_ImageRatioField_crop = ImageRatioField(
        't_ImageField',
        '1600x900',
    )
    t_ImageRatioField_free = ImageRatioField(
        't_ImageField',
        free_crop=True,
    )
    t_ImageRatioField_square = ImageRatioField(
        't_ImageField',
        '1600x1600',
    )
    t_RichTextField = RichTextField(
        'RichTextField',
        blank=True,
    )
    t_RichTextField_boolean = models.BooleanField(
        'RichTextField boolean',
        default=False,
    )
    t_TextField = models.TextField(
        'TextField',
        blank=True,
    )
    t_TextField_boolean = models.BooleanField(
        'TextField boolean',
        default=False,
    )
    t_URLField = models.URLField(
        'URLField',
        blank=True,
    )
    t_URLField_boolean = models.BooleanField(
        'URLField boolean',
        default=False,
    )
    t_VideoField_boolean = models.BooleanField(
        'VideoField boolean',
        default=False,
    )
    t_VideoField_cover = models.ImageField(
        'VideoField cover',
        blank=True,
        upload_to=file_upload_to
    )
    t_VideoField_cover_cropping = ImageRatioField(
        't_VideoField_cover',
        free_crop=True,
    )
    t_VideoField_mp4 = models.FileField(
        'VideoField mp4',
        blank=True,
        upload_to=file_upload_to,
    )
    t_VideoField_ogg = models.FileField(
        'VideoField ogg',
        blank=True,
        upload_to=file_upload_to,
    )
    t_VideoField_swf = models.FileField(
        'VideoField swf',
        blank=True,
        upload_to=file_upload_to,
    )
    t_VideoField_webm = models.FileField(
        'VideoField webm',
        blank=True,
        upload_to=file_upload_to,
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
        ordering = ['position']
        verbose_name = _('text')
        verbose_name_plural = _('texts')

    # Functions
    def __str__(self):
        return "%s %s" % (self.page.name, self.id)

    def __unicode__(self):
        return u"%s %s" % (self.page.name, self.id)

    @staticmethod
    def get_last_index():
        try:
            obj = Text.objects.order_by('-position')[0]
            return obj.position
        except IndexError:
            return 0

    def get_image(self):
        if self.t_ImageField:
            return self.t_ImageField.url
        elif self.t_FileField:
            return self.t_FileField.url

    def get_image_crop(self):
        if self.t_ImageField:
            try:
                return get_thumbnailer(self.t_ImageField).get_thumbnail({
                    'size': (1600, 0),
                    'box': self.t_ImageRatioField_crop,
                    'detail': True,
                }).url
            except InvalidImageFormatError:
                pass
        elif self.t_FileField:
            return self.t_FileField.url

    def get_image_free(self):
        if self.t_ImageField:
            try:
                return get_thumbnailer(self.t_ImageField).get_thumbnail({
                    'size': (1600, 0),
                    'box': self.t_ImageRatioField_free,
                    'detail': True,
                }).url
            except InvalidImageFormatError:
                pass
        elif self.t_FileField:
            return self.t_FileField.url

    def get_image_square(self):
        if self.t_ImageField:
            try:
                return get_thumbnailer(self.t_ImageField).get_thumbnail({
                    'size': (1600, 0),
                    'box': self.t_ImageRatioField_square,
                    'detail': True,
                }).url
            except InvalidImageFormatError:
                pass
        elif self.t_FileField:
            return self.t_FileField.url

    def get_attr(self):
        if self.t_CharField:
            return 'text'
        elif self.t_EmailField:
            return 'text'
        elif self.t_TextField:
            return 'text'
        elif self.t_ImageField:
            return 'src'
        elif self.t_FileField:
            return 'src'
        elif self.t_GeopositionField:
            return 'text'
        elif self.t_URLField:
            return 'href'
        elif self.t_RichTextField:
            return 'text'
        elif self.t_VideoField_mp4:
            return 'video'

    def get_text(self):
        if self.t_CharField:
            return self.t_CharField
        elif self.t_TextField:
            return self.t_TextField
        elif self.t_ImageField:
            return self.t_ImageField.url
        elif self.t_FileField:
            return self.t_FileField.url
        elif self.t_EmailField:
            return self.t_EmailField
        elif self.t_GeopositionField:
            return self.t_GeopositionField
        elif self.t_RichTextField:
            return mark_safe('%s' % (self.t_RichTextField))
        elif self.t_URLField:
            return self.t_URLField

    def get_value_fr(self):
        if self.t_CharField_fr:
            return self.t_CharField_fr
        elif self.t_TextField_fr:
            return self.t_TextField_fr
        elif self.t_ImageField:
            try:
                img = get_thumbnailer(self.t_ImageField).get_thumbnail({
                    'size': (400, 0),
                    'box': self.t_ImageRatioField_crop,
                    'detail': True,
                }).url
                img2 = get_thumbnailer(self.t_ImageField).get_thumbnail({
                    'size': (400, 0),
                    'box': self.t_ImageRatioField_square,
                    'detail': True,
                }).url
                return mark_safe(
                    '<img src="%s" height="100" style="margin-right: 20px;"/><img src="%s" height="100" />'
                    % (img, img2)
                )
            except InvalidImageFormatError:
                return "%s" % (_('Image File Error'))
        elif self.t_FileField:
            return mark_safe(
                '<img src="%s" height="100" style="background-color: #eee;" />' % (self.t_FileField.url)
            )
        elif self.t_EmailField:
            return self.t_EmailField
        elif self.t_URLField:
            return self.t_URLField
        elif self.t_GeopositionField:
            return self.t_GeopositionField
        elif self.t_RichTextField_fr:
            return mark_safe('%s' % (self.t_RichTextField_fr))
        elif self.t_VideoField_cover:
            try:
                img = get_thumbnailer(self.t_VideoField_cover).get_thumbnail({
                    'size': (400, 0),
                    'box': self.t_VideoField_cover_cropping,
                    'detail': True,
                }).url
                return mark_safe(
                    '<img src="%s" height="100"/>'
                    % (img)
                )
            except InvalidImageFormatError:
                return "%s" % (_('Image File Error'))
    get_value_fr.short_description = _('Value FR')

    def get_value_en(self):
        if self.t_CharField_en:
            return self.t_CharField_en
        elif self.t_TextField_en:
            return self.t_TextField_en
        elif self.t_RichTextField_en:
            return mark_safe('%s' % (self.t_RichTextField_en))
    get_value_en.short_description = _('Value EN')

    def get_value_es(self):
        if self.t_CharField_es:
            return self.t_CharField_es
        elif self.t_TextField_es:
            return self.t_TextField_es
        elif self.t_RichTextField_es:
            return mark_safe('%s' % (self.t_RichTextField_es))
    get_value_es.short_description = _('Value ES')

    def save(self, *args, **kwargs):
        if self.t_CharField:
            self.t_CharField_boolean = True
            self.t_EmailField_boolean = False
            self.t_TextField_boolean = False
            self.t_ImageField_boolean = False
            self.t_FileField_boolean = False
            self.t_GeopositionField_boolean = False
            self.t_URLField_boolean = False
            self.t_RichTextField_boolean = False
            self.t_VideoField_boolean = False
        elif self.t_EmailField:
            self.t_CharField_boolean = False
            self.t_EmailField_boolean = True
            self.t_TextField_boolean = False
            self.t_ImageField_boolean = False
            self.t_FileField_boolean = False
            self.t_GeopositionField_boolean = False
            self.t_URLField_boolean = False
            self.t_RichTextField_boolean = False
            self.t_VideoField_boolean = False
        elif self.t_TextField:
            self.t_CharField_boolean = False
            self.t_EmailField_boolean = False
            self.t_TextField_boolean = True
            self.t_ImageField_boolean = False
            self.t_FileField_boolean = False
            self.t_GeopositionField_boolean = False
            self.t_URLField_boolean = False
            self.t_RichTextField_boolean = False
            self.t_VideoField_boolean = False
        elif self.t_ImageField:
            self.t_CharField_boolean = False
            self.t_EmailField_boolean = False
            self.t_TextField_boolean = False
            self.t_ImageField_boolean = True
            self.t_FileField_boolean = False
            self.t_GeopositionField_boolean = False
            self.t_URLField_boolean = False
            self.t_RichTextField_boolean = False
            self.t_VideoField_boolean = False
        elif self.t_FileField:
            self.t_CharField_boolean = False
            self.t_EmailField_boolean = False
            self.t_TextField_boolean = False
            self.t_ImageField_boolean = False
            self.t_FileField_boolean = True
            self.t_GeopositionField_boolean = False
            self.t_URLField_boolean = False
            self.t_RichTextField_boolean = False
            self.t_VideoField_boolean = False
        elif self.t_GeopositionField:
            self.t_CharField_boolean = False
            self.t_EmailField_boolean = False
            self.t_TextField_boolean = False
            self.t_ImageField_boolean = False
            self.t_FileField_boolean = False
            self.t_GeopositionField_boolean = True
            self.t_URLField_boolean = False
            self.t_RichTextField_boolean = False
            self.t_VideoField_boolean = False
        elif self.t_URLField:
            self.t_CharField_boolean = False
            self.t_EmailField_boolean = False
            self.t_TextField_boolean = False
            self.t_ImageField_boolean = False
            self.t_FileField_boolean = False
            self.t_GeopositionField_boolean = False
            self.t_URLField_boolean = True
            self.t_RichTextField_boolean = False
            self.t_VideoField_boolean = False
        elif self.t_RichTextField:
            self.t_CharField_boolean = False
            self.t_EmailField_boolean = False
            self.t_TextField_boolean = False
            self.t_ImageField_boolean = False
            self.t_FileField_boolean = False
            self.t_GeopositionField_boolean = False
            self.t_URLField_boolean = False
            self.t_RichTextField_boolean = True
            self.t_VideoField_boolean = False
        elif self.t_VideoField_mp4:
            self.t_CharField_boolean = False
            self.t_EmailField_boolean = False
            self.t_TextField_boolean = False
            self.t_ImageField_boolean = False
            self.t_FileField_boolean = False
            self.t_GeopositionField_boolean = False
            self.t_URLField_boolean = False
            self.t_RichTextField_boolean = False
            self.t_VideoField_boolean = True
        if self.position == 0:
            self.position = Text.get_last_index() + 1
        self.t_CharField_slug = slugify(self.t_CharField_fr)
        return super(Text, self).save(*args, **kwargs)
