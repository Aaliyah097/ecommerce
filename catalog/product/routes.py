from rest_framework.routers import DefaultRouter
from catalog.product.views import ProductView
from catalog.product.image.views import ImageView
from catalog.product.spec.views import SpecsView
from catalog.product.spec.detail.views import DetailView
from catalog.product.brand.views import BrandView


product_router = DefaultRouter()
product_router.register('', ProductView, basename='product')
product_router.register('images', ImageView, basename='image')
product_router.register('specs', SpecsView, basename='spec')
product_router.register('details', DetailView, basename='detail')
product_router.register('brands', BrandView, basename='brand')
