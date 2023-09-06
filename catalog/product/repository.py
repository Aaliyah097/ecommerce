from django import forms
from django.db.models import QuerySet, Min, Max
from rest_framework.serializers import ModelSerializer, SerializerMethodField
import django_filters

from catalog.models import Products, Details, Specs, Categories, Brands
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
    price = django_filters.RangeFilter(
        field_name='price',
    )
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
        field_name='name'
    )
    description = django_filters.CharFilter(
        widget=forms.HiddenInput(),
        field_name='description'
    )
    part_number = django_filters.CharFilter(
        widget=forms.HiddenInput(),
        field_name='part_number'
    )

    @staticmethod
    def filter_by_price(queryset, name, value):
        if value == 'ascending':
            return queryset.order_by('price')
        elif value == 'descending':
            return queryset.order_by('-price')
        else:
            return queryset

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)

        # добавлять в поля фильтра по цене минимальную и максимальную цены товаров в выборке
        self.form.fields['price'].widget.widgets[0].attrs['placeholder'] = f"от {qs.aggregate(Min('price'))['price__min']}"
        self.form.fields['price'].widget.widgets[1].attrs['placeholder'] = f"до {qs.aggregate(Max('price'))['price__max']}"

        return qs

    def __init__(self, *args, **kwargs):
        try:
            category = args[0].get('category', None)
        except IndexError:
            category = None
        try:
            brand = args[0].get('brand', None)
        except IndexError:
            brand = None

        super(ProductFilter, self).__init__(*args, **kwargs)

        if category:
            details_pks = Specs.objects.filter(product__category__slug=category).values_list('detail__pk')
            brands_pks = Products.objects.filter(category__slug=category).values_list('brand__slug')

            details = Details.objects.filter(pk__in=details_pks)
            brands = Brands.objects.filter(slug__in=brands_pks)
        else:
            details = Details.objects.all()
            brands = Brands.objects.all()

        if brand:
            categories_pks = Products.objects.filter(brand__slug=brand).values_list('category__slug')
            categories = Categories.objects.filter(slug__in=categories_pks)
        else:
            categories = Categories.objects.all()

        # Выводи только те категории, которые присущи товарам выбранного бренда
        self.filters['category'] = django_filters.ModelMultipleChoiceFilter(
            field_name='category',
            label='Категории',
            queryset=categories,
            to_field_name='slug',
            widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-list'}),
        )

        # Выводим только те бренды, которые присущи выбранной категории
        self.filters['brand'] = django_filters.ModelMultipleChoiceFilter(
            field_name='brand',
            label='Производитель',
            queryset=brands,
            to_field_name='slug',
            widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-list'}),
        )

        # Выводим только те характеристики и их свойства, которые присущи товарарам в выбранной категории
        for detail in details:
            specs = Specs.objects.filter(detail=detail)
            self.filters[detail.name] = django_filters.ModelMultipleChoiceFilter(
                field_name='specs__pk',
                queryset=specs,
                to_field_name='pk',
                widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-list'}),
            )

    class Meta:
        model = Products
        fields = '__all__'


class ProductRepository:
    @staticmethod
    def get_queryset() -> QuerySet[Products]:
        return Products.objects.all().prefetch_related('specs', 'images')

    @staticmethod
    def get_by_id(pk: int) -> Products | None:
        try:
            return Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            return None
