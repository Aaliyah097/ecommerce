from rest_framework.viewsets import ModelViewSet
from catalog.product.brand.repository import (
    BrandRepository,
    BrandSerializer,
    BrandFilter
)


class BrandView(ModelViewSet):
    """product-brand view"""
    queryset = BrandRepository.get_queryset()
    serializer_class = BrandSerializer
    filterset_class = BrandFilter
