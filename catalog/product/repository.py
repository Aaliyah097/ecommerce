from catalog.models import Products
from django.db.models import QuerySet
from rest_framework.serializers import ModelSerializer, StringRelatedField
from django_filters import FilterSet

from catalog.product.image.repository import ImageSerializer
from catalog.product.spec.repository import SpecsSerializer
from catalog.product.brand.repository import BrandSerializer


class ProductSerializer(ModelSerializer):
    specs = SpecsSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    category = StringRelatedField(many=False, read_only=True)
    brand = BrandSerializer(many=False, read_only=True)

    class Meta:
        model = Products
        fields = '__all__'


class ProductFilter(FilterSet):
    class Meta:
        model = Products
        fields = '__all__'


class ProductRepository:
    @staticmethod
    def get_queryset() -> QuerySet[Products]:
        return Products.objects.all().prefetch_related('specs', 'images')
