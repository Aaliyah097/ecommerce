from django.urls import path
from catalog import views


urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('desktop', views.desktop, name='desktop'),

]
