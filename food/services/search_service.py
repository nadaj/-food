# -*- coding: utf-8 -*-
from functools import lru_cache
from food.models import ProductSpecialty
from .product_service import ProductService
from .database_service import select_column_from_queryset
import re
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet as wn
import sys


class LanguageProcessor:

    def __init__(self):
        self._stemmer = PorterStemmer()

    def stem_word(self, word):
        if "free" not in word:
            return self._stemmer.stem(word)
        return word

    @staticmethod
    def tokenize(term):
        return re.findall(r"[a-zA-Z0-9']+", term)

    @staticmethod
    def normalize(word):
        return re.sub(r"[']", '', word.lower())

    @staticmethod
    def get_synonyms(word):
        synonyms = []
        for synset in wn.synsets(word):
            lemmas = [lemma for lemma in synset.lemma_names() if lemma != word]
            for lemma in lemmas:
                synonyms.append(lemma)
        return synonyms


class SearchEngine:
    _language_processor = LanguageProcessor()

    def __init__(self):
        """
        Initializes dictionary with the cached products
        (key = keyword, value = list of matched product ids).
        """
        self._keywords = SearchEngine.init_cached_keywords()

    def find_synonyms(self, word):
        synonyms = LanguageProcessor.get_synonyms(word)
        synonym_set = set()
        for synonym in synonyms:
            splitted_synonym = LanguageProcessor.tokenize(synonym)
            splitted_synonym_list = []
            for value in splitted_synonym:
                matched = self._keywords.get(value, set())
                splitted_synonym_list.append(matched)
            splitted_synonym_set = set.intersection(*splitted_synonym_list)
            synonym_set.update(splitted_synonym_set)
        return synonym_set

    def lookup_cached_keywords(self, word, level):
        if not self._keywords:
            return None

        if level == 0:
            matched = self._keywords.get(word, set())
            matched_synonyms = self.find_synonyms(word)
            matched.update(matched_synonyms)
        else:
            matched = [value for key, value in self._keywords.items() if key.startswith(word)] if level == 1 \
                else [value for key, value in self._keywords.items() if word in key]
            if matched:
                return set.union(*matched)

        return matched if matched else None

    def find(self, search_string):
        words = LanguageProcessor.tokenize(search_string)

        for level in range(3):
            sets_of_cached_words = []
            for word in words:
                stemmed_word = self._language_processor.stem_word(word)
                normalized_word = self._language_processor.normalize(stemmed_word)
                found_set = self.lookup_cached_keywords(normalized_word, level)
                print(word + ": " + str(found_set) + "(" + str(level) + ")", file=sys.stderr)
                if not found_set:
                    found_set = set()
                sets_of_cached_words.append(found_set)

            print(sets_of_cached_words, file=sys.stderr)
            if sets_of_cached_words and bool(set.intersection(*sets_of_cached_words)):
                product_ids = set.intersection(*sets_of_cached_words)
                return ProductService.annotate_with_price(ProductService.get_products_by_ids(product_ids))

        return None

    @staticmethod
    def insert_in_cache(cached_data, key, value):
        stemmed_key = SearchEngine._language_processor.stem_word(key)
        normalized_word = SearchEngine._language_processor.normalize(stemmed_key)
        if not cached_data.get(normalized_word):
            cached_data[normalized_word] = set()
        if isinstance(value, set):
            cached_data[normalized_word].update(value)
        elif isinstance(value, int):
            cached_data[normalized_word].add(value)

    @staticmethod
    @lru_cache(maxsize=2)
    def init_cached_keywords():
        cached_data = {}

        SearchEngine.cache_data_by_names(cached_data)
        SearchEngine.cache_data_by_brands(cached_data)
        SearchEngine.cache_data_by_specialty(cached_data)
        SearchEngine.cache_data_by_departments(cached_data)

        return cached_data

    @staticmethod
    def cache_data_by_names(cached_data):
        product_names = ProductService.get_all_existing_products_names()
        for product in product_names:
            product_id = product[0]
            product_name = product[1]
            for token in LanguageProcessor.tokenize(product_name):
                SearchEngine.insert_in_cache(cached_data, token, product_id)

    @staticmethod
    def cache_data_by_brands(cached_data):
        brand_names = ProductService.get_all_existing_brand_names()
        for brand in brand_names:
            brand_id = brand[0]
            brand_name = brand[1]
            products = set(
                select_column_from_queryset(ProductService.get_products_by_brand_id(brand_id), 'id', flat=True))
            for token in LanguageProcessor.tokenize(brand_name):
                SearchEngine.insert_in_cache(cached_data, token, products)

    @staticmethod
    def cache_data_by_specialty(cached_data):
        specialties_keys = [value.name for value in ProductSpecialty._meta.fields if
                            value.name not in ['id', 'product_id', 'product']]

        specialties_filters = {}
        for key in specialties_keys:
            specialties_filters[key] = 1
            value = set(ProductService.filter_products_by_specialty(specialties_filters))
            if value:
                SearchEngine.insert_in_cache(cached_data, key, value)
            del specialties_filters[key]

    @staticmethod
    def cache_data_by_departments(cached_data):
        product_departments = ProductService.get_all_existing_products_departments()
        for department in product_departments:
            department_id = department[0]
            parent_departments = ProductService.get_departments_parents(department_id)
            products_in_department = set(
                select_column_from_queryset(ProductService.filter_products_by_department(department_id), 'id',
                                            flat=True))

            processed_departments = [item for parent_department in parent_departments
                                     for item in LanguageProcessor.tokenize(parent_department.name)]

            for processed_department in processed_departments:
                SearchEngine.insert_in_cache(cached_data, processed_department, products_in_department)

    @staticmethod
    def invalidate_cached_keywords():
        return SearchEngine.init_cached_keywords.cache_clear()

    @staticmethod
    def get_cache_info():
        return SearchEngine.init_cached_keywords.cache_info()

    def get_cache(self):
        return self._keywords
