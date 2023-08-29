from catalog.models import Brands
from django.db.models import QuerySet
from django_filters import FilterSet
from rest_framework.serializers import ModelSerializer


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brands
        fields = '__all__'


class BrandFilter(FilterSet):
    class Meta:
        model = Brands
        exclude = ('file', )


class BrandRepository:
    @staticmethod
    def get_queryset() -> QuerySet[Brands]:
        return Brands.objects.all()
