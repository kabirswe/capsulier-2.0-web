""" Models for the product app """

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from colorful.fields import RGBColorField
from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.exceptions import InvalidImageFormatError
from geoposition.fields import GeopositionField
from image_cropping.fields import ImageRatioField

from main.helpers import ActiveManager
from main import utils as main_utils

from . import utils

__author__ = 'S. M. Sazedul Haque, Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Manager
class ProductManager(models.Manager):

    def active(self, *args, **kwargs):
        return super(ProductManager, self).filter(
            active=True,
        )

    def map(self, *args, **kwargs):
        return super(ProductManager, self).filter(
            active=True,
            productextra__position_check=True
        )


# Models
class Category(models.Model):

    # Manager
    objects = ActiveManager()

    # Attributes
    active = models.BooleanField(
        _('active'),
        default=True
    )
    description = models.TextField(
        _('description'),
        blank=True
    )
    email = models.EmailField(
        _('email'),
        blank=True
    )
    slug = models.SlugField(
        _('slug'),
        max_length=206,
        unique=True,
    )
    title = models.CharField(
        _('title'),
        max_length=120,
        unique=True
    )
    image = models.ImageField(
        _('image'),
        upload_to=utils.product_upload_to,
    )
    image_cropping = ImageRatioField(
        'image',
        '1600x900',
    )
    image_cropping_square = ImageRatioField(
        'image',
        '1600x1600',
    )
    image_cropping_product = ImageRatioField(
        'image',
        '1600x1766',
    )
    ordering = models.PositiveIntegerField(
        blank=False,
        default=0,
        null=False
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

    # Meta
    class Meta:
        ordering = ['ordering']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    # Functions
    def __str__(self):
        return "%s" % (self.title)

    def __unicode__(self):
        return u"%s" % (self.title)

    # Images
    def get_image_box(self):
        if self.image:
            img = get_thumbnailer(self.image).get_thumbnail({
                'size': (400, 0),
                'box': self.image_cropping,
                'detail': True,
            }).url
            return mark_safe('<img src="%s" width="100"/>' % img)
        else:
            return "%s" % (_('None'))
    get_image_box.short_description = _('Image')

    def get_image_box_square(self):
        if self.image:
            img = get_thumbnailer(self.image).get_thumbnail({
                'size': (400, 0),
                'box': self.image_cropping_square,
                'detail': True,
            }).url
            return mark_safe('<img src="%s" width="100"/>' % img)
        else:
            return "%s" % (_('None'))

    get_image_box_square.short_description = _('Image Square')

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
        return ''

    def get_image_square_hq(self):
        if self.image:
            try:
                return get_thumbnailer(self.image).get_thumbnail({
                    'size': (1600, 0),
                    'box': self.image_cropping_square,
                    'detail': True,
                }).url
            except InvalidImageFormatError:
                pass
        else:
            pass
        return ''

    def thumbnail_image(self):
        if self.image:
            img = get_thumbnailer(self.image).get_thumbnail({
                'size': (400, 441),
                'box': self.image_cropping,
                'crop': True,
                'detail': True,
            }).url
            return img
        else:
            return None
        return ''

    # SEO
    def get_seo_description(self):
        return main_utils.get_seo_description(self.description)

    def get_seo_image(self):
        return main_utils.get_seo_image(self.image, self.image_cropping)

    def get_seo_title(self):
        return main_utils.get_seo_title(self.title)

    # Urls
    def get_absolute_url(self):
        if self.id == 1:
            return reverse('product:category_detail', kwargs={'slug': self.slug})
        return reverse('product-others:category_detail', kwargs={'slug': self.slug})

    # Others
    @staticmethod
    def get_last_index():
        try:
            obj = Category.objects.order_by('-ordering')[0]
            return obj.ordering
        except IndexError:
            return 0

    # Save
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if self.ordering == 0:
            self.ordering = Category.get_last_index() + 1
        return super(Category, self).save(*args, **kwargs)


class Feature(models.Model):

    # Relations
    product_feature_category = models.ForeignKey(
        'FeatureCategory',
        verbose_name=_('product feature category'),
    )

    # Attributes
    name = models.CharField(
        _('name'),
        max_length=128,
    )
    image = models.FileField(
        _('image'),
        blank=True,
        upload_to=utils.product_upload_to,
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
        ordering = ['product_feature_category', 'name']
        unique_together = ('name', 'product_feature_category', )
        verbose_name = _('Feature')
        verbose_name_plural = _('Features')

    # Functions
    def __str__(self):
        return "%s - %s" % (self.product_feature_category, self.name)

    def __unicode__(self):
        return u"%s - %s" % (self.product_feature_category, self.name)

    def image_tag(self):
        _('image'),
        if self.image:
            return mark_safe('<img src="%s" width="100" />' % (self.image.url))
        else:
            return "%s" % (_('None'))


class FeatureCategory(models.Model):

    # Relations
    category = models.ForeignKey(
        Category,
        verbose_name=_('category'),
    )

    # Attributes
    name = models.CharField(
        _('name'),
        max_length=128,
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

    # Meta
    class Meta:
        ordering = ['category', 'name']
        unique_together = ('category', 'name_fr', )
        verbose_name = _('Feature Category')
        verbose_name_plural = _('Features Categories')

    # Functions
    def __str__(self):
        return "%s - %s" % (self.category, self.name)

    def __unicode__(self):
        return u"%s - %s" % (self.category, self.name)


class Product(models.Model):

    # Manager
    objects = ProductManager()

    # Relations
    category = models.ForeignKey(
        'Category',
        verbose_name=_('category'),
    )
    related_products = models.ManyToManyField(
        'self',
        blank=True,
        verbose_name=_('related products'),
    )
    sites = models.ManyToManyField(
        Site,
        verbose_name=_('sites'),
    )

    # Attributes
    active = models.BooleanField(
        _('active'),
        default=True,
    )
    name = models.CharField(
        _('name'),
        max_length=128,
        unique=True,
    )
    ordering = models.PositiveIntegerField(
        blank=False,
        default=0,
        null=False
    )
    slug = models.SlugField(
        _('slug'),
        editable=False,
        max_length=206,
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
        ordering = ['ordering']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    # Functions
    def __str__(self):
        return "%s" % (self.name)

    def __unicode__(self):
        return u"%s" % (self.name)

    # Images
    def get_background_image_box(self):
        if self.productextra.background_image:
            try:
                img = get_thumbnailer(
                    self.productextra.background_image).get_thumbnail({
                        'size': (400, 0),
                        'box': self.productextra.background_image_cropping,
                        'detail': True,
                    }).url
                return mark_safe('<img src="%s" height="100" />' % img)
            except InvalidImageFormatError:
                pass
        else:
            return "%s" % (_('None'))
    get_background_image_box.short_description = _('Background Image')

    def get_background_image_hq(self):
        if self.productextra.background_image:
            try:
                return get_thumbnailer(self.productextra.background_image).get_thumbnail({
                    'size': (1600, 0),
                    'box': self.productextra.background_image_cropping,
                    'detail': True,
                }).url
            except InvalidImageFormatError:
                pass
        elif self.category.image:
            try:
                return get_thumbnailer(self.category.image).get_thumbnail({
                    'size': (1600, 0),
                    'box': self.category.image_cropping,
                    'detail': True,
                }).url
            except InvalidImageFormatError:
                pass
        else:
            pass

    def get_image_box(self):
        if self.productextra.image:
            try:
                img = get_thumbnailer(self.productextra.image).get_thumbnail({
                    'size': (400, 0),
                    'box': self.productextra.image_cropping,
                    'detail': True,
                }).url
                return mark_safe('<img src="%s" height="100" />' % img)
            except InvalidImageFormatError:
                pass
        else:
            return "%s" % (_('None'))
    get_image_box.short_description = _('Image')

    def get_image_hq(self):
        if hasattr(self, 'productextra'):
            if self.productextra.image:
                try:
                    return get_thumbnailer(self.productextra.image).get_thumbnail({
                        'size': (1600, 0),
                        'box': self.productextra.image_cropping,
                        'detail': True,
                    }).url
                except InvalidImageFormatError:
                    pass
        elif self.category.image:
            try:
                return get_thumbnailer(self.category.image).get_thumbnail({
                    'size': (1600, 0),
                    'box': self.category.image_cropping,
                    'detail': True,
                }).url
            except InvalidImageFormatError:
                pass

    def get_image_mq(self):
        if hasattr(self, 'productextra'):
            if self.productextra.image:
                try:
                    return get_thumbnailer(self.productextra.image).get_thumbnail({
                        'size': (800, 0),
                        'box': self.productextra.image_cropping,
                        'detail': True,
                    }).url
                except InvalidImageFormatError:
                    pass
        elif self.category.image:
            try:
                return get_thumbnailer(self.category.image).get_thumbnail({
                    'size': (800, 0),
                    'box': self.category.image_cropping,
                    'detail': True,
                }).url
            except InvalidImageFormatError:
                pass

    def get_image_lq(self):
        if hasattr(self, 'productextra'):
            if self.productextra.image:
                try:
                    return get_thumbnailer(self.productextra.image).get_thumbnail({
                        'size': (400, 0),
                        'box': self.productextra.image_cropping,
                        'detail': True,
                    }).url
                except InvalidImageFormatError:
                    pass
        elif self.category.image:
            try:
                return get_thumbnailer(self.category.image).get_thumbnail({
                    'size': (400, 0),
                    'box': self.category.image_cropping,
                    'detail': True,
                }).url
            except InvalidImageFormatError:
                pass

    # SEO
    def get_seo_description(self):
        return main_utils.get_seo_description(self.productlang.description)

    def get_seo_image(self):
        if hasattr(self, 'productextra'):
            if self.productextra.image:
                return self.get_image_hq()
        return main_utils.get_seo_image(self.image, self.image_cropping)

    def get_seo_title(self):
        return main_utils.get_seo_title(self.name)

    # Urls
    def get_absolute_url(self):
        if self.category.id == 1:
            return reverse('product:product_detail', kwargs={'slug': self.slug})
        return reverse('product-others:product_detail', kwargs={'slug': self.slug})

    @property
    def get_api_absolute_url(self):
        return reverse('product:product_detail', kwargs={'slug': self.slug})

    # Others
    def get_color(self):
        return self.productextra.color

    def get_description_short(self):
        return self.productlang.description_short

    def get_description_short3(self):
        return self.productlang.description_short3

    @staticmethod
    def get_last_index():
        try:
            obj = Product.objects.order_by('-ordering')[0]
            return obj.ordering
        except IndexError:
            return 0

    def get_variation_count(self):
        return self.variation_set.count()
    get_variation_count.short_description = _('Variation count')

    # Save
    def save(self, *args, **kwargs):
        if self.ordering == 0:
            self.ordering = Product.get_last_index() + 1
        self.slug = slugify(self.name)
        return super(Product, self).save(*args, **kwargs)


class ProductExtra(models.Model):

    # Relations
    product = models.OneToOneField(
        Product,
        verbose_name=_('product'),
    )
    supplier = models.ForeignKey(
        'Supplier',
        blank=True,
        null=True,
        verbose_name=_('supplier'),
    )

    # Attributes
    background_image = models.ImageField(
        _('background image'),
        blank=True,
        upload_to=utils.product_upload_to,
    )
    background_image_cropping = ImageRatioField(
        'background_image',
        '1600x1067',
    )
    color = RGBColorField(
        _('color'),
        blank=True,
    )
    description = models.TextField(
        _('description'),
        blank=True,
    )
    image = models.ImageField(
        _('image'),
        blank=True,
        upload_to=utils.product_upload_to,
    )
    image_cropping = ImageRatioField(
        'image',
        '1600x1766',
    )
    position = GeopositionField(
        _('origin'),
        blank=True,
    )
    position_check = models.BooleanField(
        default=False,
    )
    song = models.FileField(
        _('track file'),
        blank=True,
        upload_to=utils.product_upload_to,
    )
    song_artist = models.CharField(
        _('artist'),
        blank=True,
        max_length=180,
    )
    song_track_name = models.CharField(
        _('track name'),
        blank=True,
        max_length=180,
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
        ordering = ['product']
        verbose_name = _('Product Extra')
        verbose_name_plural = _('Product Extras')

    # Functions
    def __str__(self):
        return "%s" % (self.product.name)

    def __unicode__(self):
        return u"%s" % (self.product.name)

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
        elif self.product.category.image:
            try:
                return get_thumbnailer(self.product.category.image).get_thumbnail({
                    'size': (1600, 0),
                    'box': self.product.category.image_cropping,
                    'detail': True,
                }).url
            except InvalidImageFormatError:
                pass
        else:
            pass

    def save(self, *args, **kwargs):
        if self.position:
            self.position_check = True
        return super(ProductExtra, self).save(*args, **kwargs)

    def thumbnail_image(self):
        _('image'),
        if self.image:
            img = get_thumbnailer(self.image).get_thumbnail({
                'size': (400, 441),
                'box': self.image_cropping,
                'crop': True,
                'detail': True,
            }).url
            return img
        elif self.product.category.image:
            img = get_thumbnailer(self.product.category.image).get_thumbnail({
                'size': (400, 441),
                'box': self.product.category.image_cropping,
                'crop': True,
                'detail': True,
            }).url
            return img
        else:
            return None


class ProductLang(models.Model):

    # Relations
    product = models.OneToOneField(
        Product,
        verbose_name=_('product'),
    )

    # Attributes
    description = models.TextField(
        _('description'),
        blank=True,
    )
    description_short = models.CharField(
        _('description short 1'),
        blank=True,
        max_length=80,
    )
    description_short2 = models.CharField(
        _('description short 2'),
        blank=True,
        max_length=80,
    )
    description_short3 = models.CharField(
        _('description short 3'),
        blank=True,
        max_length=80,
    )
    meta_description = models.TextField(
        _('meta description'),
        blank=True,
        max_length=255,
    )
    meta_title = models.CharField(
        _('meta title'),
        blank=True,
        max_length=128,
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

    # Functions
    def __str__(self):
        return "%s" % (self.product.name)

    def __unicode__(self):
        return u"%s" % (self.product.name)

    # Meta
    class Meta:
        ordering = ['product']
        verbose_name = _('Product Lang')
        verbose_name_plural = _('Product Langs')


class ProductFeature(models.Model):

    # Relations
    feature = models.ForeignKey(
        Feature,
        verbose_name=_('feature'),
    )
    product = models.ForeignKey(
        Product,
        verbose_name=_('product'),
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
    def __str__(self):
        return "%s" % (self.feature)

    def __unicode__(self):
        return u"%s" % (self.feature)

    # Meta
    class Meta:
        ordering = ['feature']
        unique_together = ('product', 'feature', )
        verbose_name = _('Product Feature')
        verbose_name_plural = _('Product Features')


class Supplier(models.Model):

    # Attributes
    name = models.CharField(
        _('name'),
        max_length=128,
        unique=True,
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

    # Meta
    class Meta:
        ordering = ['name']
        verbose_name = _('Supplier')
        verbose_name_plural = _('Suppliers')

    # Functions
    def __str__(self):
        return "%s" % (self.name)

    def __unicode__(self):
        return u"%s" % (self.name)


class Variation(models.Model):

    # Relations
    product = models.ForeignKey(
        Product,
        verbose_name=_('product'),
    )

    # Attributes
    active = models.BooleanField(
        _('active'),
        default=True
    )
    depth = models.DecimalField(
        _('depth'),
        decimal_places=6,
        max_digits=20,
        default=0,
    )
    ean13 = models.CharField(
        _('ean13'),
        blank=True,
        max_length=13,
    )
    height = models.DecimalField(
        _('height'),
        decimal_places=6,
        max_digits=20,
        default=0,
    )
    image = models.ImageField(
        _('image'),
        blank=True,
        upload_to=utils.product_upload_to,
    )
    image_cropping = ImageRatioField(
        'image',
        '1600x1766',
    )
    inventory = models.IntegerField(
        _('inventory'),
        default=0,
    )
    on_sales = models.BooleanField(
        _('on sales'),
        default=True,
    )
    out_of_stock = models.BooleanField(
        _('out of stock'),
        default=False,
    )
    no_out_of_stock = models.BooleanField(
        _('no out of stock'),
        default=False,
    )
    price_public = models.DecimalField(
        _('public price'),
        decimal_places=2,
        default=0,
        help_text=_('VAT included'),
        max_digits=20,
    )
    price_public_ve = models.DecimalField(
        _('public price VE'),
        decimal_places=2,
        default=0,
        help_text=_('VAT excluded'),
        max_digits=20,
        editable=False,
    )
    price_pro = models.DecimalField(
        _('pro price'),
        decimal_places=2,
        default=0,
        help_text=_('VAT included'),
        max_digits=20,
    )
    price_pro_ve = models.DecimalField(
        _('pro pro VE'),
        decimal_places=2,
        default=0,
        help_text=_('VAT excluded'),
        max_digits=20,
        editable=False,
    )
    reference = models.CharField(
        _('reference'),
        blank=True,
        max_length=32,
    )
    supplier_reference = models.CharField(
        _('supplier reference'),
        blank=True,
        max_length=32,
    )
    tax_percentage = models.DecimalField(
        _('vat percentage'),
        decimal_places=3,
        default=0.055,
        max_digits=5
    )
    tax_public = models.DecimalField(
        _('public vat'),
        decimal_places=2,
        default=0,
        editable=False,
        max_digits=5,
    )
    tax_pro = models.DecimalField(
        _('pro vat'),
        decimal_places=2,
        default=0,
        editable=False,
        max_digits=5,
    )
    title = models.CharField(
        _('name'),
        max_length=120,
    )
    upc = models.CharField(
        _('upc'),
        blank=True,
        max_length=12,
    )
    weight = models.DecimalField(
        _('weight'),
        decimal_places=6,
        max_digits=20,
        default=0,
    )
    width = models.DecimalField(
        _('width'),
        decimal_places=6,
        max_digits=20,
        default=0,
    )

    # Meta data
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

    # Functions
    def __str__(self):
        return self.product.name

    def __unicode__(self):
        return self.product.name

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    @property
    def add_to_cart(self):
        return "%s?item=%s&qty=1" % (reverse('eshop:cart'), self.id)

    def remove_from_cart(self):
        return "%s?item=%s&qty=1&delete=True" % (reverse('eshop:cart'), self.id)

    def save(self, *args, **kwargs):
        self.price_public_ve = self.price_public / (1 + self.tax_percentage)
        self.price_pro_ve = self.price_pro / (1 + self.tax_percentage)
        self.tax_public = self.price_public - self.price_public_ve
        self.tax_pro = self.price_pro - self.price_pro_ve
        return super(Variation, self).save(*args, **kwargs)


def product_post_saved_receiver(sender, instance, created, *args, **kwargs):
    product = instance
    variations = product.variation_set.all()
    if variations.count() == 0:
        new_var = Variation()
        new_var.product = product
        new_var.title_fr = product.name_fr
        new_var.title_en = product.name_en
        new_var.title_es = product.name_es
        new_var.save()


post_save.connect(product_post_saved_receiver, sender=Product)


# Old
class CustomPrice(models.Model):

    # Relations
    product = models.ForeignKey(
        'Product',
        verbose_name=_('product'),
        related_name='productincustomprice',
        blank=True,
        null=True
    )
    customer = models.ForeignKey(
        User,
        verbose_name=_('customer'),
        related_name='userincustomprice',
    )

    # Attributes
    price = models.DecimalField(
        _('price'),
        decimal_places=2,
        max_digits=20,
    )

    # Meta
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
        return self.product.title

    def __unicode__(self):
        return u"%s" % (self.price)

    def get_absolute_url(self):
        return reverse('custom_price_detail', kwargs={'pk': self.pk})
