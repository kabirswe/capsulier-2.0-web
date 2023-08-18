""" API views for the catalog app """

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, filters, pagination

from .. import models
from . import serializers


__author__ = 'Sathi'
__copyright__ = 'Copyright 2018, Maison Mahdil'


# Pagination
class ResultsSetPagination(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 2


# API
class ProductList(generics.ListAPIView):
    queryset = models.Product.objects.active().order_by('-created_on')
    serializer_class = serializers.ProductListSerializer
    pagination_class = ResultsSetPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filter_fields = (
        'category',
    )
    ordering_fields = (
        'id',
    )
