# -*- coding: utf-8 -*-
from food.models import Product, Store, ProductStore, Location


class StoreService:

    @classmethod
    def all_stores(cls):
        return Store.objects.all()

    @classmethod
    def get_store_by_id(cls, store_id):
        return Store.objects.get(id=store_id)

    @classmethod
    def product_in_stores(cls, product_id):
        return ProductStore.objects.filter(product_id=product_id).order_by('price')

    @classmethod
    def all_store_locations(cls, store_id):
        return Location.objects.filter(store__id=store_id).order_by("zip_code", "city__state__abbreviation")

    @classmethod
    def get_products_available_in_store(cls, store_id):
        return Product.objects.filter(productstore__store_id=store_id).order_by("productstore__updated_at")
