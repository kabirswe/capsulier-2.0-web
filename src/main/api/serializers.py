""" Serializers for the main app """

from rest_framework import serializers

from .. import models

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Serializers
class SEOSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SEO
        fields = [
            'id',
            'page',
            'title',
            'description',
            'keywords',
            'resource_type',
            'image',
            'fb_app_id',
            'site_name',
            'twitter_site',
        ]


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Text
        fields = [
            'id',
            'page',
            'get_attr',
            'get_text',
            'get_image',
            'get_image_free',
            'get_image_square',
        ]
