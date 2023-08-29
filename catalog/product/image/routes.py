from rest_framework.routers import SimpleRouter
from catalog.product.image.views import ImageView


image_router = SimpleRouter()
image_router.register('', ImageView)
