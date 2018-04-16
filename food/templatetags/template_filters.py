from django import template

register = template.Library()


@register.filter(name='description_truncate')
def description_truncate(description, length=90, suffix="..."):
    if len(description) < length:
        return description
    else:
        return ' '.join(description[:length + 1].split(' ')[0:-1]) + suffix
