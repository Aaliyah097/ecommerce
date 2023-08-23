from catalog.models import Categories
from catalog.entities.category import Category
from functools import cache
from typing import List
from dataclasses import asdict


class CategoryRepository:
    @staticmethod
    def serialize(categories: list[Category]) -> list[dict]:
        return [asdict(cat) for cat in categories]

    @cache
    def list(self) -> list[Category]:
        base_categories = Categories.objects.filter(parent__isnull=True)
        return [
            Category(
                id=cat.id,
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
                id=child.id,
                name=child.name,
                slug=child.slug,
                children=self.get_children(child)
            )
            for child in children
        ]

    @cache
    def get_parent(self, category: Categories) -> Category | None:
        return Category(
            id=category.parent.id,
            name=category.parent.name,
            slug=category.parent.slug,
            children=self.get_children(category.parent)
        ) if category.parent else None
