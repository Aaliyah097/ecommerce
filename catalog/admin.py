from django.contrib import admin
from catalog.models import *

from mptt.admin import DraggableMPTTAdmin, TreeRelatedFieldListFilter
from rangefilter.filters import (
    NumericRangeFilterBuilder,
)


@admin.register(Categories)
class CategoriesAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count',
                    'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = (
        ('parent', TreeRelatedFieldListFilter),
    )
    search_fields = ('name', )
    search_help_text = 'Поиск по Заголовку'

    list_display_links = ['slug', ]
    list_editable = ['name', ]

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
    list_editable = ['name', 'file']


class ImagesAdmin(admin.TabularInline):
    model = Images


class ProductDetailsAdmin(admin.TabularInline):
    model = Specs


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Products._meta.fields]
    list_editable = ['part_number', 'price', 'category', 'name', 'brand']
    inlines = [
        ProductDetailsAdmin,
        ImagesAdmin
    ]
    search_fields = ('name', 'part_number')
    search_help_text = 'Поиск по Названию или Парт. номеру'
    list_filter = (
        'brand',
        'category',
        ('price', NumericRangeFilterBuilder()),
        'specs',
    )
    actions = ['export_xlsx', ]

    @admin.action(description='Экспортировать в xlsx')
    def export_xlsx(self, request, queryset):
        print(queryset)


@admin.register(Details)
class DetailsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Details._meta.fields]

    list_editable = ['name', ]
