from catalog.category.views import CategoryView
from catalog.product.views import ProductView
from catalog.product.brand.views import BrandView
from catalog.product.image.views import ImageView
from catalog.product.spec.views import SpecsView
from catalog.product.spec.detail.views import DetailView

from django.urls import path, include

from catalog.utils import get_router


urlpatterns = [
    path('categories/', include(get_router('', CategoryView))),
    path('products/', include(get_router('', ProductView))),
    path('brands/', include(get_router('', BrandView))),
    path('images/', include(get_router('', ImageView))),
    path('specs/', include(get_router('', SpecsView))),
    path('details/', include(get_router('', DetailView))),

    path('search/', include('haystack.urls')),
]
