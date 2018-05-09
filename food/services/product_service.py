# -*- coding: utf-8 -*-
from food.models import Product, ProductDepartment, ProductSpecialty
from django.db.models import Min, F


class ProductService:

    @classmethod
    def all_products(cls):
        products = Product.objects.values('productstore__product_id')
        products = ProductService.annotate_with_price(products)
        products = products.values()
        return products

    @classmethod
    def filter_products_by_name(cls, name):
        products = cls.all_products()
        return products.filter(name__icontains=name)

    @classmethod
    def filter_products_by_department(cls, department_id):
        products = cls.all_products()
        return products.filter(department_id=department_id)

    @classmethod
    def filter_products_by_specialty(cls, specialty):
        return ProductSpecialty.objects.values_list('product_id', flat=True).filter(**specialty)

    @classmethod
    def get_product_by_id(cls, product_id):
        return Product.objects.get(id=product_id)

    @classmethod
    def get_products_by_ids(cls, product_ids):
        return Product.objects.filter(id__in=product_ids)

    @classmethod
    def get_products_by_brand_id(cls, brand_id):
        return Product.objects.filter(brand_id=brand_id)

    @classmethod
    def annotate_with_price(cls, query_set):
        return query_set.annotate(brand_name=F('brand__name'), price=Min('productstore__price'),
                                  created_at=F('productstore__created_at'))

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

    @classmethod
    def get_all_existing_products_departments(cls):
        return Product.objects.all().values_list('department_id', 'department__name').distinct()

    @classmethod
    def get_all_existing_products_names(cls):
        return Product.objects.all().values_list('id', 'name').order_by('id')

    @classmethod
    def get_all_existing_brand_names(cls):
        return Product.objects.all().values_list('brand_id', 'brand__name').distinct()

    @classmethod
    def sort_products(cls, products, sort_parameter):
        if sort_parameter == 'name_asc_rank':
            return products.extra(order_by=['name'])
        elif sort_parameter == 'name_desc_rank':
            return products.extra(order_by=['-name'])
        elif sort_parameter == 'price_asc_rank':
            return products.extra(order_by=['price'])
        elif sort_parameter == 'price_desc_rank':
            return products.extra(order_by=['-price'])
        elif sort_parameter == 'date_desc_rank':
            return products.extra(order_by=['-created_at'])

        return products
