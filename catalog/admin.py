from django.contrib import admin
from catalog.models import *


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Categories._meta.fields]


@admin.register(Brands)
class BrandsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Brands._meta.fields]


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Products._meta.fields]


@admin.register(Details)
class DetailsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Details._meta.fields]


@admin.register(ProductDetails)
class ProductDetailsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductDetails._meta.fields]


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Images._meta.fields]
