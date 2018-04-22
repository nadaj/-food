# -*- coding: utf-8 -*-


def select_column_from_queryset(query_set, column_name, flat=False):
    return query_set.values_list(column_name, flat=flat)

