from catalog.category.routes import category_router
from catalog.product.routes import product_router
from django.urls import path, include


urlpatterns = [
    path('categories/', include(category_router.urls)),
    path('products/', include(product_router.urls)),
]
