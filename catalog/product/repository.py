import django.forms.widgets

from catalog.models import Products
from django.db.models import QuerySet
from rest_framework.serializers import ModelSerializer, SerializerMethodField
import django_filters
from django.forms import widgets

from catalog.product.image.repository import ImageSerializer
from catalog.product.spec.repository import SpecsSerializer
from catalog.product.brand.repository import BrandSerializer, Brands


class ProductSerializer(ModelSerializer):
    specs = SpecsSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    brand_info = SerializerMethodField(read_only=True)

    @staticmethod
    def get_brand_info(obj):
        return BrandSerializer(obj.brand).data

    class Meta:
        model = Products
        fields = '__all__'


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Products
        exclude = '__all__'


class ProductRepository:
    @staticmethod
    def get_queryset() -> QuerySet[Products]:
        return Products.objects.all().prefetch_related('specs', 'images')
