from catalog.models import Specs
from django.db.models import QuerySet
from django_filters import FilterSet
from rest_framework.serializers import ModelSerializer


from catalog.product.spec.detail.repository import DetailSerializer


class SpecsSerializer(ModelSerializer):
    detail = DetailSerializer(many=False)

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
