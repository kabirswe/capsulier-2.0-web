""" API serializers for the catalog app """

from rest_framework import serializers

from .. import models

__author__ = 'Sathi'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Serializer
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = [
            'id',
            'title',
        ]


class ProductExtraSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductExtra
        fields = [
            'id',
            'color',
        ]


class ProductLangSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductLang
        fields = [
            'id',
            'description_short',
            'description_short2',
            'description_short3',
        ]


class VariationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Variation
        fields = [
            'id',
            'inventory',
            'no_out_of_stock',
            'price_pro',
            'price_public',
        ]


class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=False)
    productextra = ProductExtraSerializer(many=False, read_only=False)
    productlang = ProductLangSerializer(many=False, read_only=False)
    variation_set = VariationSerializer(many=True, read_only=False)

    class Meta:
        model = models.Product
        fields = [
            'id',
            'category',
            'get_absolute_url',
            'get_image_hq',
            'name',
            'productextra',
            'productlang',
            'variation_set',
        ]
