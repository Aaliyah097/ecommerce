from django.urls import path
from catalog import views


urlpatterns = [
    path('categories', views.categories, name='catalog'),
]
