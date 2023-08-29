from rest_framework.routers import SimpleRouter
from catalog.product.spec.views import SpecsView


spec_router = SimpleRouter()
spec_router.register('', SpecsView)
