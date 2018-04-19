# -*- coding: utf-8 -*-
from django.db import models
from decimal import Decimal


class ProductBrand(models.Model):
    name = models.CharField(max_length=100, unique=True)


class ProductDepartment(models.Model):
    department = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, unique=True)


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(default='')
    quantity_in_kilo = models.DecimalField(max_digits=2, decimal_places=2, default=0)
    barcode = models.CharField(max_length=50, unique=True, default='')
    image = models.CharField(max_length=2083,
                             default='https://s3.amazonaws.com/nadaj-food/product_images/No_Image_Available.gif')
    # (many-to-one) brand has multiple products, but a product has only 1 brand
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(ProductDepartment, on_delete=models.CASCADE, null=True)

    # many-to-many
    stores = models.ManyToManyField('Store', through='ProductStore')

    def metric_to_pounds(self):
        return Decimal(self.quantity_in_kilo) * Decimal('2.2')


class ProductSpecialty(models.Model):
    kosher = models.BooleanField(default=False)
    gluten_free = models.BooleanField(default=False)
    organic = models.BooleanField(default=False)
    vegan = models.BooleanField(default=False)
    vegetarian = models.BooleanField(default=False)
    dairy_free = models.BooleanField(default=False)
    low_fat = models.BooleanField(default=False)
    sugar_free = models.BooleanField(default=False)
    keto = models.BooleanField(default=False)
    paleo = models.BooleanField(default=False)
    # (one-to-one) each product is defined by specialty
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
    )


class Store(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    products = models.ManyToManyField(Product, through='ProductStore')
    image = models.CharField(max_length=2083,
                             default='https://s3.amazonaws.com/nadaj-food/store_images/No_Image_Available.gif')


class State(models.Model):
    name = models.CharField(max_length=15, unique=True)
    abbreviation = models.CharField(max_length=2, unique=True)


class City(models.Model):
    name = models.CharField(max_length=50)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)


class Location(models.Model):
    name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=5)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)


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
