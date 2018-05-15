# -*- coding: utf-8 -*-
from django.db import models
from food.models.product import Product
from food.models.store import Store


class ProductStore(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_kilo = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # to provide unique pair of product-store
    class Meta:
        unique_together = ('product', 'store')
