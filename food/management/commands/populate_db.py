import os
from bs4 import BeautifulSoup
import string
from food.models import Product, ProductBrand, ProductStore, ProductSpecialty
import uuid
from django.core.management.base import BaseCommand
from random import randint


def strip_unprintable(data):
    return ''.join(str(c) for c in data if str(c) in string.printable)


def get_data():
    os.chdir(r"C:/Users/Nada/Desktop/datasets/wholefoods")

    soup = BeautifulSoup(open(r"Whole Foods Market - Ice Cream & Ice(Three Twins).html", encoding="utf-8"),
                         "html.parser")

    price_divs = soup.findAll('div', {'class': 'item-price'})
    prices = []
    for price in price_divs:
        prices.append(price.span.span.text[1:])

    name_divs = soup.findAll('span', {'class': 'full-item-name'})
    names = []
    for name in name_divs:
        names.append(strip_unprintable(name.text))

    # # BRANDS
    # brands = []
    # brand_divs_parent = soup.find('h3', {'id': 'search-filter-brand'}).parent
    # brand_divs = brand_divs_parent.findAll('li', {'class': 'single-filter-option'})
    # for brand in brand_divs:
    #     brands.append(brand.text)

    return dict(zip(names, prices))


class Command(BaseCommand):
    """
    Call in console: py manage.py populate_db
    """
    help = 'Inserts data into database.'

    def handle(self, *args, **options):
        # # INSERT RANDOM SPECIALTIES
        for id in range(1, 659):
            if Product.objects.filter(id=id).exists() and not ProductSpecialty.objects.filter(product_id=id).exists():
                product_specialty = ProductSpecialty.objects.get_or_create(product_id=id, kosher=randint(0, 1),
                                                                       gluten_free=randint(0, 1), organic=randint(0, 1),
                                                                       vegan=randint(0, 1), vegetarian=randint(0, 1),
                                                                       dairy_free=randint(0, 1), low_fat=randint(0, 1),
                                                                       sugar_free=randint(0, 1), keto=randint(0, 1),
                                                                       paleo=randint(0, 1))
        # for name, price in get_data().items():
        #     print(name)
        # # # PRODUCT INSTATIATION
        # if not Product.objects.filter(name=name).exists():
        #     barcode = uuid.uuid4().hex[:10]
        #     product_instance = Product.objects.get_or_create(name=name, barcode=barcode, brand_id=52,
        #                                                      department_id=145)

        # # # PRODUCT_STORE INSTANTIATION
        # product = Product.objects.get(name=name)
        # store_id = 1
        # product_in_store_instance = ProductStore.objects.get_or_create(price=price, product_id=product.id,
        #                                                                store_id=1)

        # # # BRAND INSTANTIATION
        # brand_instance = ProductBrand.objects.get_or_create(name=brand)
