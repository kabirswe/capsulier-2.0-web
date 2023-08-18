""" Models for the blog app """

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from ckeditor_uploader.fields import RichTextUploadingField
from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.exceptions import InvalidImageFormatError
from image_cropping.fields import ImageRatioField

from main.helpers import ActiveManager
from main import utils as main_utils

from . import utils

__author__ = 'Alamgir Kabir Roni, Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Models
class Author(models.Model):

    # Attributes
    first_name = models.CharField(
        _('first name'),
        max_length=50,
    )
    last_name = models.CharField(
        _('last name'),
        max_length=50,
    )
    slug = models.SlugField(
        _('slug'),
        editable=False,
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

    # Functions
    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        self.slug = '-'.join(
            [slugify(self.first_name), slugify(self.last_name)]
        )
        return super(Author, self).save(*args, **kwargs)

    # Meta
    class Meta:
        ordering = ['first_name']
        unique_together = ('first_name', 'last_name',)
        verbose_name = _('author')
        verbose_name_plural = _('authors')


class Image(models.Model):

    # Relations
    post = models.ForeignKey(
        'Post',
        verbose_name=_('post'),
    )

    # Attributes
    image = models.ImageField(
        _('image'),
        upload_to=utils.blog_upload_to,
    )
    image_cropping = ImageRatioField(
        'image',
        free_crop=True,
        verbose_name='free crop',
    )
    image_cropping_square = ImageRatioField(
        'image',
        '900x900',
        verbose_name='900x900',
    )
    ordering = models.PositiveIntegerField(
        blank=False,
        default=0,
        null=False
    )

    # Meta
    class Meta:
        ordering = ['ordering']
        verbose_name = _('image')
        verbose_name_plural = _('images')

    # Functions
    def __str__(self):
        return "%s - %s" % (self.post.title, self.ordering)

    def __unicode__(self):
        return u"%s - %s" % (self.post.title, self.ordering)

    @staticmethod
    def get_last_index():
        try:
            obj = Image.objects.order_by('-ordering')[0]
            return obj.ordering
        except IndexError:
            return 0

    def get_image_hq(self):
        if self.image:
            try:
                return get_thumbnailer(self.image).get_thumbnail({
                    'size': (800, 0),
                    'box': self.image_cropping,
                    'detail': True,
                }).url
            except InvalidImageFormatError:
                pass
        else:
            pass
        return ""

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
        else:
            pass
        return ""

    def save(self, *args, **kwargs):
        if self.ordering == 0:
            self.ordering = Image.get_last_index() + 1
        return super(Image, self).save(*args, **kwargs)


class Post(models.Model):

    # Manager
    objects = ActiveManager()

    # Relations
    author = models.ForeignKey(
        Author,
        verbose_name=_('author'),
        related_name=_('post_by_author')
    )
    credit_photo = models.ForeignKey(
        Author,
        verbose_name=_('credit photo'),
        related_name=_('post_by_credit_photo'),
        blank=True,
        null=True,
    )
    sites = models.ManyToManyField(
        Site,
        verbose_name=_('sites'),
    )

    # Attributes
    abstract = models.TextField(
        _('abstract'),
        blank=True,
    )
    active = models.BooleanField(
        _('active'),
        default=True,
    )
    content = RichTextUploadingField(
        _('content'),
        blank=True,
    )
    published_date = models.DateField(
        _('published date'),
    )
    slug = models.SlugField(
        _('slug'),
        editable=False,
        unique=True,
    )
    title = models.CharField(
        _('title'),
        max_length=200,
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
        return "%s" % (self.title)

    def __unicode__(self):
        return u"%s" % (self.title)

    # Meta
    class Meta:
        ordering = ['-published_date']
        verbose_name = _('post')
        verbose_name_plural = _('posts')

    # SEO
    def get_seo_description(self):
        return main_utils.get_seo_description(self.abstract)

    def get_seo_image(self):
        if self.image_set.first():
            return self.image_set.first().get_image_hq()
        return main_utils.get_seo_image(self.image, self.image_cropping)

    def get_seo_title(self):
        return main_utils.get_seo_title(self.title)

    # Urls
    def get_absolute_url(self):
        return reverse('blog:blog_detail', kwargs={'slug': self.slug})

    # Save
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title_fr)
        return super(Post, self).save(*args, **kwargs)
