from dataclasses import dataclass, asdict
from typing import Iterator

from django.contrib.sessions.backends.db import SessionStore


class CartItem:
    def __init__(self, product_id: int, name: str, price: float = 0, amount: int = 1):
        self.product_id: str = str(product_id)
        self.name: str = name
        self.price: float = price
        self.amount: int = amount
        self._cost: float = 0

    def __add__(self, other):
        self.amount += other.amount

    def __iadd__(self, other):
        self.amount += other.amount
        return self

    def __sub__(self, other):
        self.amount -= other.amount

    def __isub__(self, other):
        self.amount -= other.amount
        return self

    def __str__(self):
        return str(self.serialize())

    @property
    def cost(self) -> float:
        return self.amount * self.price

    def serialize(self) -> dict:
        return {
            'product_id': self.product_id,
            'name': self.name,
            'price': self.price,
            'amount': self.amount,
            'cost': self.cost
        }

    @staticmethod
    def deserialize(item: dict) -> 'CartItem':
        return CartItem(
            product_id=item['product_id'],
            name=item['name'],
            price=item['price'],
            amount=item['amount']
        )


class Cart:
    def __init__(self, session: SessionStore):
        self.session = session

        cart = self.session.get('cart', None)
        if not cart:
            cart = self.session['cart'] = {}

        self._cart: dict[str, dict] = cart

    # признак наличия в корзине
    def in_cart(self, item: CartItem) -> bool:
        return item.product_id in self._cart

    # количество товаров в корзине
    def __len__(self) -> int:
        return sum([CartItem.deserialize(item).amount for item in self._cart.values()])

    # стоимость всей корзины
    def cost(self) -> float:
        return sum([CartItem.deserialize(item).cost for item in self._cart.values()])

    # очистить корзину
    def clear(self) -> None:
        del self.session['cart']
        self.session.modified = True

    # добавить товар
    def add(self, item: CartItem) -> None:
        if self.in_cart(item):
            current_item = CartItem.deserialize(self._cart[item.product_id])
            current_item += item
            item = current_item

        self._cart[item.product_id] = item.serialize()
        self.session.modified = True

    # уменьшить количество товара на 1
    def sub(self, item: CartItem) -> None:
        if not self.in_cart(item):
            return

        current_item = CartItem.deserialize(self._cart[item.product_id])
        current_item -= item

        if current_item.amount == 0:
            self.dell(item)
        else:
            self._cart[item.product_id] = current_item.serialize()

        self.session.modified = True

    # удалить товар из корзины
    def dell(self, item: CartItem) -> None:
        if not self.in_cart(item):
            return
        else:
            del self._cart[item.product_id]

        self.session.modified = True

    # получить список товаров в корзине
    @property
    def items(self) -> list[CartItem]:
        return [CartItem.deserialize(item) for item in self._cart.values()]
