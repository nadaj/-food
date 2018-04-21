# -*- coding: utf-8 -*-
from food.models import Product, ProductDepartment
from django.db.models import Min, F


class ProductService:

    @classmethod
    def all_products(cls):
        products = Product.objects.values('productstore__product_id').annotate(brand_name=F('brand__name'),
                                                                               price=Min('productstore__price'))
        products = products.values()
        return products

    @classmethod
    def filter_products_by_name(cls, name):
        products = cls.all_products()
        return products.filter(name__icontains=name)

    @classmethod
    def get_product_by_id(cls, product_id):
        return Product.objects.get(id=product_id)

    @classmethod
    def get_departments_parents(cls, department_id):
        query = "SELECT T2.id, T2.name " \
                "FROM (" \
                "   SELECT @r AS _id, (SELECT @r := department_id " \
                "                      FROM food_productdepartment " \
                "                      WHERE id = _id) AS department_id, @l := @l + 1 AS lvl " \
                "   FROM (SELECT @r := '%d', @l := 0) vars, food_productdepartment " \
                "   WHERE @r <> 0) T1 " \
                "JOIN food_productdepartment T2 ON T1._id = T2.id " \
                "ORDER BY T1.lvl DESC" % department_id
        return ProductDepartment.objects.raw(query)
