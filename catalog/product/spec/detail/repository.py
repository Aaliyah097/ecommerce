from catalog.models import Details
from django.db.models import QuerySet
from django_filters import FilterSet
from rest_framework.serializers import ModelSerializer


class DetailSerializer(ModelSerializer):
    class Meta:
        model = Details
        fields = '__all__'


class DetailFilter(FilterSet):
    class Meta:
        model = Details
        fields = '__all__'


class DetailRepository:
    @staticmethod
    def get_queryset() -> QuerySet[Details]:
        return Details.objects.all()
