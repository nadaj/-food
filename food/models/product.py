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

    class Meta:
        ordering = ['id']


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
