from rest_framework import serializers
from django.db.models import QuerySet
import django_filters

from catalog.models import Categories
from catalog.category.entity import Category
from functools import cache
from typing import List
from dataclasses import asdict


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Categories
        fields = '__all__'


class CategoryRepository:
    @staticmethod
    def get_queryset() -> QuerySet[Categories]:
        return Categories.objects.all()

    @staticmethod
    def serialize(categories: list[Category] | Category) -> list[dict]:
        if type(categories) == list:
            return [asdict(cat) for cat in categories]
        else:
            return asdict(categories)

    @cache
    def tree(self) -> list[Category]:
        base_categories = Categories.objects.filter(parent__isnull=True)
        return [
            Category(
                name=cat.name,
                slug=cat.slug,
                children=self.get_children(cat)
            )
            for cat in base_categories
        ]

    @cache
    def get_children(self, category: Categories) -> List[Category]:
        children = Categories.objects.filter(parent=category)

        return [
            Category(
                name=child.name,
                slug=child.slug,
                children=self.get_children(child)
            )
            for child in children
        ]
