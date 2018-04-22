# -*- coding: utf-8 -*-
from functools import lru_cache
from food.models import ProductSpecialty
from .product_service import ProductService
from .database_service import select_column_from_queryset
import re


class SearchEngine:

    def __init__(self):
        """
        Initializes dictionary with the cached products
        (key = keyword, value = list of matched product ids).
        """
        self._cached_keywords = SearchEngine.init_cached_keywords()

    def lookup_cached_keywords(self, word):
        if self._cached_keywords is not None:
            return self._cached_keywords.get(word)
        return None

    def find(self, search_string):
        words = search_string.split()
        sets_of_cached_words = []

        for word in words:
            found_set = self.lookup_cached_keywords(word)
            if found_set:
                sets_of_cached_words.append(found_set)

        if sets_of_cached_words:
            return set.intersection(*sets_of_cached_words)
        else:
            return None

    @staticmethod
    def word_segmentation(term):
        return re.findall(r"[\w']+", term)

    @staticmethod
    @lru_cache(maxsize=2)
    def init_cached_keywords():
        cached_keyword_dictionary = {}

        # CACHE DATA BY SPECIALTY
        specialties_keys = [value.name for value in ProductSpecialty._meta.fields if
                            value.name not in ['id', 'product_id', 'product']]
        specialties_filters = {}
        for key in specialties_keys:
            specialties_filters[key] = 1
            value = set(ProductService.filter_products_by_specialty(specialties_filters))
            if value:
                cached_keyword_dictionary[key] = value
            del specialties_filters[key]

        # CACHE DATA BY DEPARTMENTS
        product_departments = ProductService.get_all_existing_products_departments()
        for department in product_departments:
            department_id = department[0]
            parent_departments = ProductService.get_departments_parents(department_id)
            products_in_department = set(
                select_column_from_queryset(ProductService.filter_products_by_department(department_id), 'id',
                                            flat=True))

            processed_departments = [item for parent_department in parent_departments
                                     for item in SearchEngine.word_segmentation(parent_department.name.lower())]

            for processed_department in processed_departments:
                cached_keyword_dictionary[processed_department] = products_in_department

        return cached_keyword_dictionary

    @staticmethod
    def invalidate_cached_keywords():
        return SearchEngine.init_cached_keywords.cache_clear()

    @staticmethod
    def get_cache_info():
        return SearchEngine.init_cached_keywords.cache_info()

    def get_cache(self):
        return self._cached_keywords
