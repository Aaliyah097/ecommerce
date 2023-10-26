import datetime
from copy import deepcopy

from django import forms
from django.db.models import QuerySet, Min, Max, F
from pycbrf import ExchangeRates
from rest_framework.serializers import ModelSerializer, SerializerMethodField
import django_filters

from catalog.utils import update_rates
from catalog.models import Products, Details, Specs, Categories, Brands, Currencies
from catalog.product.image.repository import ImageSerializer
from catalog.product.spec.repository import SpecsSerializer
from catalog.product.brand.repository import BrandSerializer
from catalog.category.repository import CategorySerializer


class ProductSerializer(ModelSerializer):
    specs = SpecsSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    brand_info = SerializerMethodField(read_only=True)
    category_info = SerializerMethodField(read_only=True)

    @staticmethod
    def get_brand_info(obj):
        return BrandSerializer(obj.brand).data

    @staticmethod
    def get_category_info(obj):
        return CategorySerializer(obj.category).data

    class Meta:
        model = Products
        fields = '__all__'


class ProductFilter(django_filters.FilterSet):
    price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        label='Цена до',
        method='filter_price'
    )
    # price = django_filters.NumberFilter(
    #     field_name='price',
    #     widget=forms.HiddenInput()
    # )
    order_by_price = django_filters.ChoiceFilter(
        method='filter_by_price',
        label='Упорядочить по цене',
        choices=(
            ('ascending', 'По возврастанию'),
            ('descending', 'По убыванию')
        ),
        widget=forms.RadioSelect()
    )
    name = django_filters.CharFilter(
        widget=forms.HiddenInput(),
        field_name='name',
        lookup_expr='icontains'
    )
    description = django_filters.CharFilter(
        widget=forms.HiddenInput(),
        field_name='description'
    )
    part_number = django_filters.CharFilter(
        widget=forms.TextInput(),
        field_name='part_number',
        lookup_expr='iexact'
    )
    source = django_filters.CharFilter(
        widget=forms.HiddenInput(),
        field_name='source'
    )
    source_link = django_filters.CharFilter(
        widget=forms.HiddenInput(),
        field_name='source_link'
    )
    image_link = django_filters.CharFilter(
        widget=forms.HiddenInput(),
        field_name='image_link'
    )
    category = django_filters.CharFilter(
        field_name='category',
        label='Категории',
        method='filter_category_name'
    )

    def filter_price(self, queryset, name, value):
        rate = float(ExchangeRates(str(datetime.date.today()))['USD'].rate)
        not_in = []
        for q in queryset:
            if q.price * rate <= value:
                not_in.append(q.pk)
        return queryset.filter(pk__in=not_in)

    def filter_brand_name(self, queryset, name, value):
        value = value.replace("[", "").replace("]", "").replace("'", "")
        value = value.split(",")

        for v in value:
            if v != '':
                break
        else:
            return queryset

        return queryset.filter(brand__slug=value)

    def filter_category_name(self, queryset, name, value):
        value = value.replace("[", "").replace("]", "").replace("'", "")
        value = value.split(",")
        for v in value:
            if v != '':
                break
        else:
            return queryset.filter(category__parent__isnull=True)

        return queryset.filter(
            category__in=Categories.objects.filter(slug__in=value).get_descendants(include_self=True))

    @staticmethod
    def filter_by_price(queryset, name, value):
        if value == 'ascending':
            return queryset.order_by('price')
        elif value == 'descending':
            return queryset.order_by('-price')
        else:
            return queryset

    class Meta:
        model = Products
        exclude = ('currency', )


class ProductRepository:
    @staticmethod
    def get_queryset() -> QuerySet[Products]:
        return Products.objects.all().prefetch_related('specs', 'images')

    @staticmethod
    def get_by_id(pk: int) -> Products:
        try:
            return Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            return None
