from django.contrib import admin
from django.utils.safestring import mark_safe

from catalog.models import *
from catalog.category.repository import CategoryForm

from mptt.admin import DraggableMPTTAdmin, TreeRelatedFieldListFilter
from django.contrib.admin import DateFieldListFilter
from rangefilter.filters import (
    NumericRangeFilterBuilder,
)

from catalog.utils import update_rates


@admin.register(Currencies)
class CurrenciesAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol')


@admin.register(Categories)
class CategoriesAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count',
                    'name', 'slug', 'is_hidden')
    list_editable = ('is_hidden', )
    prepopulated_fields = {'slug': ('name',)}
    list_filter = (
        ('parent', TreeRelatedFieldListFilter),
        'is_hidden'
    )
    search_fields = ('name', )
    search_help_text = 'Поиск по Заголовку'
    form = CategoryForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Categories.objects.add_related_count(
            qs,
            Products,
            'category',
            'products_cumulative_count',
            cumulative=True)

        # Add non cumulative product count
        qs = Categories.objects.add_related_count(qs,
                                                  Products,
                                                  'category',
                                                  'products_count',
                                                  cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count

    related_products_count.short_description = 'Товаров в категории'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count

    related_products_cumulative_count.short_description = 'Товаров в ветке'


@admin.register(Brands)
class BrandsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Brands._meta.fields]
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    search_help_text = 'Поиск по Названию'
    list_display_links = ['slug', ]
    list_editable = ['name', 'file', 'is_hidden', 'image_link']
    list_filter = ['is_hidden', ]


class ImagesAdmin(admin.TabularInline):
    model = Images
    extra = 0


class SpecsAdmin(admin.TabularInline):
    model = Specs
    extra = 0


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Products._meta.fields if field.name not in ['description', 'image_link', 'source_link']]
    # list_editable = ['part_number', 'price', 'category', 'name', 'brand', 'currency', ]
    inlines = [
        SpecsAdmin,
        ImagesAdmin
    ]
    search_fields = ('part_number', 'series', 'id')
    search_help_text = 'Поиск по Названию, Серии или Парт. номеру'
    list_filter = (
        'brand',
        'category',
        ('price', NumericRangeFilterBuilder()),
        'specs',
        'currency',
        'source',
    )
    actions = ['export_xlsx', ]

    @admin.action(description='Экспортировать в xlsx')
    def export_xlsx(self, request, queryset):
        pass


@admin.register(Details)
class DetailsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Details._meta.fields]
    search_fields = ['name', ]
    list_editable = ['name', ]


class OrderItemsAdmin(admin.TabularInline):
    model = OrderItems
    extra = 0
    raw_id_fields = ['product']


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_items', 'get_total_cost', 'rate', 'status', 'created_at', 'updated_at', 'discount', 'client', 'comment']
    list_editable = ['status', 'discount', 'client', 'comment', 'rate']
    inlines = [OrderItemsAdmin, ]
    search_fields = ['id', 'client']
    list_filter = ['status']

    def get_total_cost(self, obj):
        items = OrderItems.objects.filter(order=obj)
        if obj.rate:
            for item in items:
                item.product.price = item.product.price * obj.rate
                item.in_currency = item.product.price / obj.rate
        else:
            update_rates([item.product for item in items])

        return mark_safe(f"{round(sum([item.product.price * item.amount for item in items]) * ((100 - obj.discount) / 100), 2)} RUB" + "<br><br>")

    def get_items(self, obj):
        items = OrderItems.objects.filter(order=obj)
        return mark_safe('<br><br>'.join([f"{item.product.category.name if item.product.category else None} {item.product.brand.name if item.product.brand else None} {item.product.part_number if item.product else None} {item.amount if item else None} шт." for item in items]))

    get_items.short_description = "Товары в заказе"
    get_total_cost.short_description = "Итого"
