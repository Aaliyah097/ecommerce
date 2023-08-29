from catalog.models import Images
from django.db.models import QuerySet
from django_filters import FilterSet
from rest_framework.serializers import ModelSerializer


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'


class ImageFilter(FilterSet):
    class Meta:
        model = Images
        exclude = ('file', )


class ImageRepository:
    @staticmethod
    def get_queryset() -> QuerySet[Images]:
        return Images.objects.all()
