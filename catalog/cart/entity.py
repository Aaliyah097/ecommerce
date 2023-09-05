from dataclasses import dataclass, asdict
from typing import Iterator

from django.contrib.sessions.backends.db import SessionStore


@dataclass
class CartItem:
    product_id: int
    name: str
    price: float = 0
    amount: int = 1
    _cost: float = 0

    def __add__(self, other):
        self.amount += other.amount

    def __sub__(self, other):
        self.amount -= other.amount

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


class Cart:
    def __init__(self, session: SessionStore):
        self.session = session

        cart = self.session.get('cart', None)
        if not cart:
            cart = self.session['cart'] = {}

        self._cart: dict[int, CartItem] = cart

    # признак наличия в корзине
    def in_cart(self, item: CartItem) -> bool:
        return item.product_id in self._cart

    # количество товаров в корзине
    def __len__(self) -> int:
        return sum([item.amount for item in self._cart.values()])

    # стоимость всей корзины
    def cost(self) -> float:
        return sum([item.cost for item in self._cart.values()])

    # очистить корзину
    def clear(self) -> None:
        del self.session['cart']
        self.session.modified = True

    # добавить товар
    def add(self, item: CartItem) -> None:
        if not self.in_cart(item):
            self._cart[item.product_id] = item
        else:
            self._cart[item.product_id] += item

    # уменьшить количество товара на 1
    def sub(self, item: CartItem) -> None:
        if not self.in_cart(item):
            return
        else:
            self._cart[item.product_id] -= item

        if self._cart[item.product_id].amount == 0:
            self.dell(item)

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
        return [item for item in self._cart.values()]
