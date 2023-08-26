from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view

from catalog.urls import urlpatterns as catalog_urls
from web import urls as web_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include(catalog_urls)),
    path('web/', include(web_urls)),

    path('openapi/', get_schema_view(
        title="E-com",
        description="Catalog Management System",
        version="1.0.0"
    ), name='openapi-schema'),
]
