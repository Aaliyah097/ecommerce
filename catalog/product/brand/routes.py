from rest_framework.routers import SimpleRouter
from catalog.product.brand.views import BrandView


brand_router = SimpleRouter()
brand_router.register('', BrandView)
