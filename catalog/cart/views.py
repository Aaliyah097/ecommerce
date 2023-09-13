from rest_framework.decorators import APIView, action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from catalog.cart.entity import Cart, CartItem
from catalog.product.repository import ProductRepository


class CartView(APIView):
    renderer_classes = [JSONRenderer, ]

    @staticmethod
    def get_cart_item(product_id: int) -> CartItem:
        product = ProductRepository.get_by_id(product_id)

        if not product:
            return None

        return CartItem(
            product_id=product_id,
            name=product.name,
            price=product.price,
            amount=1
        )

    def post(self, request, pk: int):
        """Добавить или увеличить кол-во на 1"""
        cart = Cart(request.session)

        cart_item = self.get_cart_item(pk)

        if not cart_item:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=f"Товара в id {pk} не существует"
            )

        cart.add(cart_item)

        return Response(
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk: int):
        """Уменьшить количество на 1 или удалить если количество станет равно 0"""
        cart = Cart(request.session)

        cart_item = self.get_cart_item(pk)

        if not cart_item:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=f"Товара в id {pk} не существует"
            )

        cart.sub(cart_item)

        return Response(
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk: int):
        """Удалить из корзины"""
        cart = Cart(request.session)

        cart_item = self.get_cart_item(pk)

        if not cart_item:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=f"Товара в id {pk} не существует"
            )

        cart.dell(cart_item)

        return Response(
            status=status.HTTP_200_OK,
        )

    def get(self, request):
        """
        **Посмотреть корзину**
        **Ответ**: 200
        ```python
        {
            "products": [
                {
                    'product_id': '0',
                    'name': '',
                    'price': 0,
                    'amount': 0,
                    'cost': 0
                }
            ],
            "amount": 0,
            "cost": 0
        }
        ```
        """
        cart = Cart(request.session)

        return Response(
            status=status.HTTP_200_OK,
            data={
                'products': [item.serialize() for item in cart.items],
                'amount': len(cart),
                'cost': cart.cost()
            }
        )
