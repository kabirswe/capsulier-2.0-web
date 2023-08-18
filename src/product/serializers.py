""" API serializers for the page app """

from rest_framework import serializers

from . import models

__author__ = 'Shamima Akter Shampa, Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Serializers
class ProductExtraSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.ProductExtra
        fields = (
            'id',
            'position',
            'thumbnail_image',
        )


class ProductLangSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.ProductLang
        fields = (
            'id',
            'description',
        )


class ProductCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = (
            'id',
            'description',
        )


class ProductSerializers(serializers.ModelSerializer):
    productextra = ProductExtraSerializers(
        many=False,
        read_only=True,
    )
    productlang = ProductLangSerializers(
        many=False,
        read_only=True,
    )
    category = ProductCategorySerializers(
        many=False,
        read_only=True,
    )

    class Meta:
        model = models.Product
        fields = (
            'id',
            'category',
            'name',
            'sites',
            'productextra',
            'productlang',
            'get_api_absolute_url',
            'get_image_lq',
        )
