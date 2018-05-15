# -*- coding: utf-8 -*-
from django.db import models


class Store(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    products = models.ManyToManyField('Product', through='ProductStore')
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
    phone = models.CharField(max_length=15, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
