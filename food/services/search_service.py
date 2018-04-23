# -*- coding: utf-8 -*-
from functools import lru_cache
from food.models import ProductSpecialty
from .product_service import ProductService
from .database_service import select_column_from_queryset
import re
from nltk.stem import PorterStemmer


class LanguageProcessor:

    def __init__(self):
        self._stemmer = PorterStemmer()

    def stem_word(self, word):
        if "free" not in word:
            return self._stemmer.stem(word)
        return word

    @staticmethod
    def tokenize_by_word(term):
        return re.findall(r"[a-zA-Z0-9']+", term)


class SearchEngine:
    _language_processor = LanguageProcessor()

    def __init__(self):
        """
        Initializes dictionary with the cached products
        (key = keyword, value = list of matched product ids).
        """
        self._cached_keywords = SearchEngine.init_cached_keywords()

    def lookup_cached_keywords(self, word):
        if not self._cached_keywords:
            return None
        return self._cached_keywords.get(word)

    def find(self, search_string):
        words = LanguageProcessor.tokenize_by_word(search_string)
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
                stemmed_key = SearchEngine._language_processor.stem_word(key)
                cached_keyword_dictionary[stemmed_key] = value
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
                                     for item in LanguageProcessor.tokenize_by_word(parent_department.name.lower())]

            for processed_department in processed_departments:
                stemmed_key = SearchEngine._language_processor.stem_word(processed_department)
                cached_keyword_dictionary[stemmed_key] = products_in_department

        return cached_keyword_dictionary

    @staticmethod
    def invalidate_cached_keywords():
        return SearchEngine.init_cached_keywords.cache_clear()

    @staticmethod
    def get_cache_info():
        return SearchEngine.init_cached_keywords.cache_info()

    def get_cache(self):
        return self._cached_keywords
