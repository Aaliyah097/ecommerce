import sys
import os
import django
import openpyxl
import requests


sys.path.append(os.path.join(os.path.dirname(__file__), 'ecommerce'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")
django.setup()

from django.db import transaction
from catalog.models import *
from bs4 import BeautifulSoup


def import_routers_switch(page: str):
    wb = openpyxl.load_workbook(r"C:\Users\Aaliyah\dev\gamma\routers-switch.com-cards.xlsx")
    sheet = wb[page]
    source = 'www.router-switch.com'
    currency = Currencies.objects.get(name='USD')
    for row_number in range(2, sheet.max_row + 1):
        if row_number < 0:
            continue
        product = {
            'source': source,
            'part_number': sheet.cell(row_number, 1).value,
            'category': sheet.cell(row_number, 2).value,
            'brand': sheet.cell(row_number, 3).value,
            'sub_cat1': sheet.cell(row_number, 4).value,
            'sub_cat2': sheet.cell(row_number, 5).value,
            'sub_cat3': sheet.cell(row_number, 6).value,
            'series': sheet.cell(row_number, 7).value,
            'link': sheet.cell(row_number, 8).value,
            'price': sheet.cell(row_number, 9).value,
            'name': sheet.cell(row_number, 10).value,
            'picture_link': sheet.cell(row_number, 11).value,
            'specs': sheet.cell(row_number, 12).value or None
        }
        # specs = []
        # if product['specs']:
        #     soup = BeautifulSoup(product['specs'], 'html.parser')
        #     rows = soup.find_all('tr')
        #     for row in rows:
        #         columns = row.find_all('td')
        #         if len(columns) == 0 or len(columns) < 2:
        #             continue
        #         sign, value = columns[0].text, columns[1].text
        #         specs.append((sign, value))

        brand = Brands.objects.get(name=product['brand'])
        category = Categories.objects.get(slug=product['category'].lower())

        new_product = Products(
            name=product['name'],
            category=category,
            part_number=product['part_number'],
            brand=brand,
            price=product['price'],
            currency=currency,
            description=product['specs'],
            source=source,
            source_link=product['link'],
            series=product['series'],
            image_link=product['picture_link']
        )
        try:
            new_product = Products.objects.get(part_number=product['part_number'], brand=brand)
        except Products.DoesNotExist:
            new_product.save()
        #     new_product = Products.objects.get(part_number=product['part_number'], brand=brand)
        #
        # new_image = Images(
        #     product=new_product,
        #     image_link=product['picture_link']
        # )
        # new_image.save()

        # for sign, value in specs:
        #     detail = Details.objects.filter(name__icontains=sign).first()
        #     if not detail:
        #         new_detail = Details(name=sign)
        #         new_detail.save()
        #         detail = Details.objects.filter(name__icontains=sign).first()
        #
        #     new_spec = Specs(
        #         detail=detail,
        #         product=new_product,
        #         value=value
        #     )
        #     try:
        #         spec = Specs.objects.get(detail=detail, product=new_product)
        #     except Specs.DoesNotExist:
        #         new_spec.save()


if __name__ == '__main__':
    import_routers_switch('routers')
