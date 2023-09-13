from io import BytesIO
import os
import logging
import requests

from spellchecker import SpellChecker
from pycbrf import ExchangeRates
import datetime
import openpyxl

from catalog.models import Products, Currencies
from django.db.models import QuerySet
from rest_framework.routers import DefaultRouter


logger = logging.getLogger(__name__)


def get_google_sheet_data() -> dict:
    sheet_id = os.environ.get('GOOGLE_SHEET_ID')
    sheet_range = 'A1:Z10000'
    api_key = os.environ.get('GOOGLE_API_KEY')

    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{sheet_range}?key={api_key}"
    return requests.get(url).json()


def clean_price(price: str) -> float:
    price = str(price).replace('р.', "").replace(",", ".").replace(" ", "").replace("$", "").replace('\xa0', "")
    try:
        return float(price)
    except TypeError:
        return None


def export_xlsx(products: QuerySet[Products]) -> BytesIO:
    pass


def update_rates(products: list[Products]):
    try:
        currency = Currencies.objects.get(name='RUB')
    except Currencies.DoesNotExist:
        currency = None

    daily_rates = ExchangeRates(str(datetime.date.today()))

    if currency:
        for product in products:
            if product.currency == currency:
                continue
            rate = daily_rates[product.currency.name]
            product.currency = currency
            product.price = round(float(rate.rate) * product.price, 0)

    return products


def get_router(name: str, view) -> list:
    r = DefaultRouter()
    r.register(name, view)
    return r.urls


def check_spell(words: str) -> str:
    spell = SpellChecker(language=['ru', 'en'], distance=1)

    words = remove_spaces(words)
    misspelled = spell.unknown(words.split(' ')).union(set([w.lower() for w in words.split(' ')]))

    result = []
    for word in misspelled:
        correction = spell.correction(word)
        result.append(correction if correction else word)

    return ' '.join(result)


def remove_spaces(value: str) -> str:
    value = str(value)
    splitted_value = list(value)

    pass_begin = False
    pass_end = False

    for _ in splitted_value:
        if not pass_begin:
            if splitted_value[0] == " ":
                del splitted_value[0]
            else:
                pass_begin = True

        if not pass_end:
            if splitted_value[-1] == " ":
                del splitted_value[-1]
            else:
                pass_end = True

        if pass_end and pass_begin:
            break

    return ''.join(splitted_value)