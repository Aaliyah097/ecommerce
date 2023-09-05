from rest_framework.decorators import action, APIView
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from rest_framework import status
from rest_framework.renderers import JSONRenderer


class CartView(APIView):
    renderer_classes = [JSONRenderer, ]

    def post(self, request, pk: int):
        return Response(
            status=status.HTTP_200_OK,
            data='post'
        )

    def put(self, request, pk: int):
        return Response(
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk: int):
        return Response(
            status=status.HTTP_200_OK,
            data='delete'
        )

    def get(self, request):
        return Response(
            status=status.HTTP_200_OK,
            data='get'
        )
