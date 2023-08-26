from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from catalog.category.repository import (
    CategoryRepository,
    CategorySerializer,
)


class CategoryView(ViewSet):
    """categories as tree"""
    queryset = CategoryRepository.get_queryset()
    serializer_class = CategorySerializer

    def list(self, request):
        repo = CategoryRepository()

        return Response(
            status=status.HTTP_200_OK,
            data=repo.serialize(repo.list())
        )
