""" Helpers for the main app """

from django.db import models
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _

from easy_thumbnails.exceptions import InvalidImageFormatError
from easy_thumbnails.files import get_thumbnailer

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Images
def get_image(image_field, cropping_field, thumb_size):
    if image_field:
        try:
            return get_thumbnailer(image_field).get_thumbnail({
                'size': (thumb_size, 0),
                'box': cropping_field,
                'detail': True,
            }).url
        except InvalidImageFormatError:
            pass
    return ''


def get_profile_image(image_field, cropping_field, thumb_size):
    if image_field:
        try:
            return get_thumbnailer(image_field).get_thumbnail({
                'size': (thumb_size, thumb_size),
                'box': cropping_field,
                'detail': True,
            }).url
        except InvalidImageFormatError:
            pass
    return ''


# Functions
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
            return "%s" % (_('Image File Error'))
    else:
        return "%s" % (_('None'))


def get_marker_box(self):
    if self.marker:
        try:
            img = get_thumbnailer(self.marker).url
            return mark_safe('<img src="%s" height="40" />' % img)
        except InvalidImageFormatError:
            return "%s" % (_('Image File Error'))
    else:
        return "%s" % (_('None'))


def make_active(modeladmin, request, queryset):
    for i in queryset:
        i.active = True
        i.save()


def make_inactive(modeladmin, request, queryset):
    for i in queryset:
        i.active = False
        i.save()


# Functions descriptions
get_image_box.short_description = _('Image')
make_active.short_description = _('Mark selected active')
make_inactive.short_description = _('Mark selected inactive')


# Managers
class ActiveManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(ActiveManager, self).filter(
            active=True,
        )
