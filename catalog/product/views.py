from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from catalog.product.repository import (
    ProductRepository,
    ProductSerializer,
    ProductFilter,
    Products
)
from haystack.query import SearchQuerySet


class ProductView(ModelViewSet):
    """product with joined images and spec"""
    queryset = ProductRepository.get_queryset()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter

    @action(methods=['GET', ], detail=False, url_name='search')
    def search(self, request):
        q = request.GET.get('q', '')

        results = SearchQuerySet().models(Products).filter(content=q)

        return Response(
            status=status.HTTP_200_OK,
            data=self.serializer_class([r.object for r in results], many=True).data
        )

    # def list(self, request, *args, **kwargs):
    #     qs = self.filterset_class(request.GET, queryset=self.queryset).qs
    #     return Response(
    #         status=status.HTTP_200_OK,
    #         data=self.serializer_class(qs, many=True).data
    #     )

    @action(methods=['GET', ], detail=False, url_name='autocomplete')
    def autocomplete(self, request):
        query = request.GET.get('term', '')

        results = SearchQuerySet().autocomplete(content=query)

        result = [{'label': f"{product.brand.name} {product.category.name} {product.part_number}", 'value': product.part_number} for product in [r.object for r in results]]

        return Response(
            status=status.HTTP_200_OK,
            data=result
        )
