""" Serializers for the main app """

from rest_framework import serializers

from .. import models

__author__ = 'Alamgir Kabir Roni'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Serializers
class ConceptMapSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.ConceptMap
        fields = (
            'id',
            'address',
            'marker',
            'name',
        )
