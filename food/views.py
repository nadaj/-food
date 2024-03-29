# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from food.services.product_service import ProductService
from food.services.store_service import StoreService
from food.services.search_service import SearchEngine, LanguageProcessor


def index(request):
    return render(request, 'index.html', {})


def all_products(request):
    sorting_values = zip(
        ['Sort by:', 'Name: A-Z', 'Name: Z-A', 'Price: ascending', 'Price: descending', 'Newest arrivals'],
        ['relevance', 'name_asc_rank', 'name_desc_rank', 'price_asc_rank', 'price_desc_rank',
         'date_desc_rank'])
    search_parameter = request.GET.get('search-products-bar', '')
    sort_parameter = request.GET.get('sort_products', 'relevance')
    page = request.GET.get('page', 1)

    if search_parameter:
        search_engine = SearchEngine()
        SearchEngine.init_cached_keywords()
        products = search_engine.find(search_parameter)
        # # DEBUG
        # with open("cached_data.txt", "w") as file:
        #     for key, value in search_engine.get_cache().items():
        #         file.write(key + ": " + str(value) + "\n")
    else:
        products = ProductService.all_products()

    if not products:
        return render(request, 'products_list.html',
                      {"products": None, "search_parameter": search_parameter, "sort_parameter": sort_parameter,
                       "sorting_values": sorting_values})

    if sort_parameter != 'relevance':
        products = ProductService.sort_products(products, sort_parameter)

    paginator = Paginator(products, 10)
    try:
        products_paginated = paginator.page(page)
    except PageNotAnInteger:
        products_paginated = paginator.page(1)
    except EmptyPage:
        products_paginated = paginator.page(paginator.num_pages)

    return render(request, 'products_list.html', {"products": products_paginated, "search_parameter": search_parameter,
                                                  "sort_parameter": sort_parameter, "sorting_values": sorting_values})


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
