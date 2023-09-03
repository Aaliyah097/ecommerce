from rest_framework.viewsets import ModelViewSet
from catalog.product.brand.repository import (
    BrandRepository,
    BrandSerializer,
    BrandFilter
)
from catalog.utils import FormViewMixin


class BrandView(ModelViewSet, FormViewMixin):
    """product-entities view"""
    queryset = BrandRepository.get_queryset()
    serializer_class = BrandSerializer
    filterset_class = BrandFilter
