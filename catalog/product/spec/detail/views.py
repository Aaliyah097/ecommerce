from rest_framework.viewsets import ModelViewSet
from catalog.product.spec.detail.repository import (
    DetailRepository,
    DetailSerializer,
    DetailFilter
)


class DetailView(ModelViewSet):
    """spec view"""
    queryset = DetailRepository.get_queryset()
    serializer_class = DetailSerializer
    filterset_class = DetailFilter
