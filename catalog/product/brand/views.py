from rest_framework.parsers import MultiPartParser, FileUploadParser, JSONParser, FormParser
from rest_framework.viewsets import ModelViewSet
from catalog.product.brand.repository import (
    BrandRepository,
    BrandSerializer,
    BrandFilter
)


class BrandView(ModelViewSet):
    """product-entities view"""
    queryset = BrandRepository.get_queryset()
    serializer_class = BrandSerializer
    filterset_class = BrandFilter
    parser_classes = [FormParser, MultiPartParser, ]
