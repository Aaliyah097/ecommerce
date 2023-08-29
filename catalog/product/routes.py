from rest_framework.routers import SimpleRouter
from catalog.product.views import ProductView


product_router = SimpleRouter()
product_router.register('', ProductView)
