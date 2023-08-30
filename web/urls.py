from django.urls import path
from web import views


urlpatterns = [
    path('', views.index, name='index'),
    path('brands', views.brands, name='brands'),
]
