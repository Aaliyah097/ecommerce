from django.urls import path
from catalog.category.views import *


urlpatterns = [
    path('categories/', list_view, name='list'),
    path('categories/update/', update_view, name='update'),
    path('categories/delete/', delete_view, name='delete'),
    path('categories/<int:pk>/', retrieve_view, name='retrieve'),
    path('categories/create/', create_view, name='create'),
]
