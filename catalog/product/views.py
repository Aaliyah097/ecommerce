from rest_framework.viewsets import ModelViewSet
from catalog.product.repository import (
    ProductRepository,
    ProductSerializer,
    ProductFilter
)


class ProductView(ModelViewSet):
    """product with joined images and spec"""
    queryset = ProductRepository.get_queryset()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
