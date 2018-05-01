# -*- coding: utf-8 -*-
from django.shortcuts import render
from food.services.product_service import ProductService
from food.services.store_service import StoreService
from food.services.search_service import SearchEngine, LanguageProcessor


def index(request):
    return render(request, 'index.html', {})


def all_products(request):
    search_parameter = request.GET.get('search-products-bar')
    res = None
    if search_parameter:
        search_engine = SearchEngine()
        SearchEngine.init_cached_keywords()
        # products = ProductService.filter_products_by_name(search_parameter)
        products = search_engine.find(search_parameter)
        res = search_engine.get_cache()
        synonyms = LanguageProcessor.get_synonyms("icecream")
    else:
        products = ProductService.all_products()
    return render(request, 'products_list.html', {"products": products, "res": res, "synonyms": synonyms})


def product_details(request, product_id):
    if request.method == 'GET':
        product = ProductService.get_product_by_id(product_id)
        if product:
            product_in_stores = StoreService.product_in_stores(product_id)
            departments = ProductService.get_departments_parents(product.department.id)
        return render(request, 'product_details.html',
                      {"product": product, "product_in_stores": product_in_stores, "departments": departments})
    else:
        return render(request, 'products_list.html', {})


def all_stores(request):
    stores = StoreService.all_stores()
    return render(request, 'stores_list.html', {"stores": stores})


def store_details(request, store_id):
    if request.method == 'GET':
        store = StoreService.get_store_by_id(store_id)
        locations = StoreService.all_store_locations(store_id)
        products = StoreService.get_products_available_in_store(store)[:5]
        return render(request, 'store_details.html', {"store": store, "locations": locations, "products": products})
    else:
        return render(request, 'stores_list.html', {})


def show_about(request):
    return render(request, 'about.html')


def show_contact(request):
    return render(request, 'contact.html')
