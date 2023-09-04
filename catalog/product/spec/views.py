from rest_framework.viewsets import ModelViewSet
from catalog.product.spec.repository import (
    SpecsRepository,
    SpecsSerializer,
    SpecsFilter
)


class SpecsView(ModelViewSet):
    """product-spec view"""
    queryset = SpecsRepository.get_queryset()
    serializer_class = SpecsSerializer
    filterset_class = SpecsFilter
