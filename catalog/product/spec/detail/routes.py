from rest_framework.routers import SimpleRouter
from catalog.product.spec.detail.views import DetailView


detail_router = SimpleRouter()
detail_router.register('', DetailView)
