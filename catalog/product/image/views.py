from rest_framework.viewsets import ModelViewSet
from catalog.product.image.repository import (
    ImageRepository,
    ImageSerializer,
    ImageFilter
)
from catalog.utils import FormViewMixin


class ImageView(ModelViewSet, FormViewMixin):
    """product-images view"""
    queryset = ImageRepository.get_queryset()
    serializer_class = ImageSerializer
    filterset_class = ImageFilter
