from django import template
from math import ceil
register = template.Library()


@register.filter(name='description_truncate')
def description_truncate(description, length=90, suffix="..."):
    if len(description) < length:
        return description
    else:
        return ' '.join(description[:length + 1].split(' ')[0:-1]) + suffix


@register.simple_tag(name='range')
def get_range(start, end):
    return range(start, end)


@register.simple_tag(name='min')
def minimum(first, second):
    return min(first, second)


@register.simple_tag(name='max')
def maximum(first, second):
    return max(first, second)


@register.simple_tag(name='add')
def addition(first, second):
    return first + second


@register.simple_tag(name='generate_page_range')
def generate_page_range(current_page, display_pages):
    left_part = current_page - ceil(display_pages / 2)
    if left_part < 1:
        left_part = current_page - 1
    right_part = current_page + display_pages - (current_page - left_part)
    return range(left_part, right_part)
