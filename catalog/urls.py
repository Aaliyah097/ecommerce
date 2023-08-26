from catalog.category.routes import category_router
from django.urls import path, include


urlpatterns = [
    path('categories/', include(category_router.urls)),
]