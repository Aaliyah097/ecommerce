from django.urls import path
from dashboard import views


urlpatterns = [
    path('', views.index, name='index'),
    path('brands', views.brands, name='brands'),
]
