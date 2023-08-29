from rest_framework.routers import DefaultRouter
from catalog.category.views import CategoryView


category_router = DefaultRouter()
category_router.register('', CategoryView, basename='category')
