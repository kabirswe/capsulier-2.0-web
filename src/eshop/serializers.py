""" API serializers for the eshop app """

from rest_framework import serializers

from product.models import Variation, Product

from . import models

__author__ = 'Aupourbau Koumar'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Serializers
class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name',
            # 'weight',
            'id',
            'productextra',
            'category',
            'get_image_lq',
            'get_description_short',
            'get_description_short3',
            'get_color',
        )


class VariationSerializers(serializers.ModelSerializer):
    product = ProductSerializers(many=False, read_only=True)

    class Meta:
        model = Variation
        fields = (
            'product',
            'id',
            'title',
            'price_pro',
            'price_public',
            'add_to_cart',
        )


class PackageSerializers(serializers.ModelSerializer):
    product = ProductSerializers(many=False, read_only=True)

    class Meta:
        model = Variation
        fields = (
            'product',
            'id',
            'price',
        )


class CartForItemSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.Cart
        fields = (
            'subtotal',
            'get_subtotal_vi',
            'total',
            'tax_total',
        )


class CartItemSerializers(serializers.ModelSerializer):
    cart = CartForItemSerializers(many=False, read_only=True)
    item = VariationSerializers(many=False, read_only=True)

    class Meta:
        model = models.CartItem
        fields = (
            'id',
            'cart',
            'item',
            'line_item_total',
            'quantity',
            'remove',
            'unit_price',
        )


class CartSerializers(serializers.ModelSerializer):
    cartitem_set = CartItemSerializers(many=True, read_only=True)

    class Meta:
        model = models.Cart
        fields = (
            'cartitem_set',
            'subtotal',
            'get_subtotal_vi',
            'total',
            'tax_total',
            'discount_total',
            'shipping_total',
        )
