from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from django.views.generic import TemplateView
from drf_yasg import openapi

from catalog.urls import urlpatterns as catalog_urls
from web import urls as web_urls


schema_view = get_schema_view(
    openapi.Info(
        title="E-com",
        default_version='v.1.0.0',
        description="REST Product Catalog Management System",
        contact=openapi.Contact(email="name.boltz@gmail.com"),
    ),
    public=True,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include(catalog_urls)),
    path('web/', include(web_urls)),

    path(
        'swagger/',
        TemplateView.as_view(
            template_name='swagger.html',
            extra_context={'schema_url': 'openapi-schema'}
        ),
        name='swagger'),
    path('swagger/<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
