from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from catalog.product.repository import (
    ProductRepository,
    ProductSerializer,
    ProductFilter,
    Products
)
from catalog.utils import FormViewMixin
from haystack.query import SearchQuerySet


class ProductView(ModelViewSet, FormViewMixin):
    """product with joined images and spec"""
    queryset = ProductRepository.get_queryset()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter

    @action(methods=['GET', ], detail=False, url_name='search')
    def search(self, request, *args, **kwargs):
        q = request.GET.get('q', '')

        results = SearchQuerySet().models(Products).filter(content=q)

        return Response(
            status=200,
            data=self.serializer_class([r.object for r in results], many=True).data
        )
