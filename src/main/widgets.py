""" Widgets for the main app """

from django import forms
from django.utils.html import mark_safe

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Widgets
class ImageWidget(forms.ClearableFileInput):
    """
    A ImageField Widget that shows a thumbnail.
    """

    def __init__(self, attrs={}):
        super(ImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        output.append(
            super(ImageWidget, self).render(name, value, attrs)
        )
        if value and hasattr(value, 'url'):
            output.append((
                '<br/> <a rel="facebox" target="_blank" href="%s">'
                '<img class="photo" src="%s" style="height: 200px;" /></a>'
                % (value.url, value.url))
            )
        return mark_safe(u''.join(output))
