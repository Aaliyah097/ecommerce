from django.urls import path
from web import views


urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.catalog_page, name='catalog'),
    path('about/', views.about_page, name='about'),
    path('contacts/', views.contacts_page, name='contacts'),
    path('category/<str:slug>', views.category_page, name='category'),
    path('product/<str:brand_slug>/<str:part_number>', views.product_page, name='product'),
]
