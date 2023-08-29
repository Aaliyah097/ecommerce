from catalog.category.routes import category_router
from catalog.product.routes import product_router
from catalog.product.brand.routes import brand_router
from catalog.product.image.routes import image_router
from catalog.product.spec.routes import spec_router
from catalog.product.spec.detail.routes import detail_router

from django.urls import path, include

# include((catalog_urls, 'catalog'), namespace='catalog')
urlpatterns = [
    path('categories/', include(category_router.urls)),
    path('products/', include(product_router.urls)),
    path('brands/', include(brand_router.urls)),
    path('images/', include(image_router.urls)),
    path('specs/', include(spec_router.urls)),
    path('details/', include(detail_router.urls)),
]
