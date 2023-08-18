""" API Views for the main app """

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from .. import models
from . import serializers

__author__ = 'Alamgir Kabir Roni'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# API Views
class ConceptMapAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = models.ConceptMap.objects.all()
    serializer_class = serializers.ConceptMapSerializers
