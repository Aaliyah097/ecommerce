import json

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from catalog.category.repository import (
    CategoryRepository,
    CategorySerializer,
)


class CategoryView(ModelViewSet):
    """categories as tree"""
    queryset = CategoryRepository.get_queryset()
    serializer_class = CategorySerializer

    def list(self, request, **kwargs):
        repo = CategoryRepository()

        return Response(
            status=status.HTTP_200_OK,
            data=json.dumps(repo.serialize(repo.list()))
        )
