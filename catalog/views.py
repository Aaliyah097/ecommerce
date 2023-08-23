from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json


@api_view(['GET', ])
def catalog(request):
    from catalog.repositories.category_repository import CategoryRepository

    repo = CategoryRepository()

    return HttpResponse(
        status=status.HTTP_200_OK,
        content=repo.serialize(repo.list())
    )
