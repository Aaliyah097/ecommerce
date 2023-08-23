from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status
import json

from catalog.category.repository import CategoryRepository


@api_view(['GET', ])
def list_view(request):
    repo = CategoryRepository()

    return HttpResponse(
        status=status.HTTP_200_OK,
        content=json.dumps(repo.serialize(repo.list()))
    )


@api_view(['UPDATE', ])
def update_view(request):
    repo = CategoryRepository()

    name = request.GET.get('name', None)
    slug = request.GET.get('slug', None)
    parent_id = request.GET.get('parent_id', None)
    category_id = request.GET.get('id', None)

    repo.update(category_id, name, slug, parent_id)

    return HttpResponse(
        status=status.HTTP_200_OK,
    )


@api_view(['DELETE', ])
def delete_view(request):
    repo = CategoryRepository()

    category_id = request.GET.get('id', None)

    repo.delete_by_id(category_id)

    return HttpResponse(
        status=status.HTTP_200_OK,
    )


@api_view(['GET', ])
def retrieve_view(request, pk):
    repo = CategoryRepository()

    category = repo.get_by_id(pk)

    return HttpResponse(
        status=status.HTTP_200_OK,
        content=json.dumps(repo.serialize(category))
    )


@api_view(['POST', ])
def create_view(request):
    repo = CategoryRepository()

    name = request.GET.get('name', None)
    slug = request.GET.get('slug', None)
    parent_id = request.GET.get('parent_id', None)

    repo.create(name, slug, parent_id)

    return HttpResponse(
        status=status.HTTP_200_OK,
    )

