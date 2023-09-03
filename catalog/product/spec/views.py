from rest_framework.viewsets import ModelViewSet
from catalog.product.spec.repository import (
    SpecsRepository,
    SpecsSerializer,
    SpecsFilter
)
from catalog.utils import FormViewMixin


class SpecsView(ModelViewSet, FormViewMixin):
    """product-spec view"""
    queryset = SpecsRepository.get_queryset()
    serializer_class = SpecsSerializer
    filterset_class = SpecsFilter
