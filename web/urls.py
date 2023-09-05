from django.urls import path
from web import views


urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.catalog_page, name='catalog_page'),
]
