from catalog.models import Specs
from django.db.models import QuerySet
from django_filters import FilterSet
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from catalog.product.spec.detail.repository import DetailSerializer


class SpecsSerializer(ModelSerializer):
    detail_info = SerializerMethodField(read_only=True)

    @staticmethod
    def get_detail_info(obj):
        return DetailSerializer(obj.detail).data

    class Meta:
        model = Specs
        fields = '__all__'


class SpecsFilter(FilterSet):
    class Meta:
        model = Specs
        fields = '__all__'


class SpecsRepository:
    @staticmethod
    def get_queryset() -> QuerySet[Specs]:
        return Specs.objects.all()
