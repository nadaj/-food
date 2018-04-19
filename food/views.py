# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.db.models import Min, F
from food.models import Product, Store, ProductStore, ProductDepartment, Location


def index(request):
    return render(request, 'index.html', {})


def all_products(request):
    search_parameter = request.GET.get('search-products-bar')
    products = Product.objects.values('productstore__product_id').annotate(brand_name=F('brand__name'),
                                                                           price=Min('productstore__price'))
    products = products.values()
    if search_parameter:
        return products_search_list(request, products, search_parameter)
    return render(request, 'products_list.html', {"products": products})


def products_search_list(request, products, search_parameter):
    products = products.filter(name__icontains=search_parameter)
    return render(request, 'products_list.html', {"products": products})


def product_details(request, identifier):
    if request.method == 'GET':
        product = Product.objects.get(id=identifier)
        if product:
            product_in_stores = ProductStore.objects.filter(product_id=identifier).order_by('price')
            query = "SELECT T2.id, T2.name " \
                    "FROM (" \
                    "   SELECT @r AS _id, (SELECT @r := department_id " \
                    "                      FROM food_productdepartment " \
                    "                      WHERE id = _id) AS department_id, @l := @l + 1 AS lvl " \
                    "   FROM (SELECT @r := '%d', @l := 0) vars, food_productdepartment " \
                    "   WHERE @r <> 0) T1 " \
                    "JOIN food_productdepartment T2 ON T1._id = T2.id " \
                    "ORDER BY T1.lvl DESC" % product.department.id
            departments = ProductDepartment.objects.raw(query)
        return render(request, 'product_details.html',
                      {"product": product, "product_in_stores": product_in_stores, "departments": departments})
    else:
        return render(request, 'products_list.html', {})


def all_stores(request):
    stores = Store.objects.all()
    return render(request, 'stores_list.html', {"stores": stores})


def store_details(request, identifier):
    if request.method == 'GET':
        store = Store.objects.get(id=identifier)
        locations = Location.objects.filter(store__id=identifier).order_by("zip_code", "city__state__abbreviation")
        query = locations.query
        return render(request, 'store_details.html', {"store": store, "locations": locations})
    else:
        return render(request, 'stores_list.html', {})


def show_about(request):
    return render(request, 'about.html')


def show_contact(request):
    return render(request, 'contact.html')
