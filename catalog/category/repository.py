from catalog.models import Categories
from catalog.category.entity import Category
from functools import cache
from typing import List
from dataclasses import asdict


class CategoryRepository:
    @staticmethod
    def serialize(categories: list[Category] | Category) -> list[dict]:
        if type(categories) == list:
            return [asdict(cat) for cat in categories]
        else:
            return asdict(categories)

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

    def get_by_id(self, category_id) -> Category | None:
        try:
            category = Categories.objects.get(id=category_id)
        except Categories.DoesNotExist:
            return None

        return Category(
            id=category.id,
            name=category.name,
            slug=category.slug,
            children=self.get_children(category)
        )

    @staticmethod
    def _get_by_id(category_id: int) -> Categories | None:
        try:
            category = Categories.objects.get(id=category_id)
        except Categories.DoesNotExist:
            return None

        return category

    def delete_by_id(self, category_id: int) -> None:
        if not category_id:
            return None

        category = self._get_by_id(category_id)
        if category:
            category.delete()

    def create(self, name: str, slug: str, parent_id: int = None) -> None:
        if not all([name, slug, parent_id]):
            return None

        parent = self._get_by_id(parent_id)

        new_category = Categories(
            name=name,
            slug=slug,
            parent=parent
        )
        new_category.save()

    def update(self, category_id: int, name: str, slug: str, parent_id: int) -> None:
        if not all([category_id, name, slug]):
            return None

        category = self._get_by_id(category_id)
        if not category:
            return None

        parent = self._get_by_id(parent_id)

        category.name = name
        category.slug = slug
        category.parent = parent

        category.save()

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
