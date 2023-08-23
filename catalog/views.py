from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
from django.shortcuts import render


@api_view(['GET', ])
def categories(request):
    from catalog.repositories.category_repository import CategoryRepository

    repo = CategoryRepository()

    return HttpResponse(
        status=status.HTTP_200_OK,
        content=repo.serialize(repo.list())
    )

