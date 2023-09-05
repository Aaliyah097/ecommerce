from django.urls import path
from web import views


urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products_page, name='products_page'),
]
