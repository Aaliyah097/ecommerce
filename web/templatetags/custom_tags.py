from django import template
import re

register = template.Library()


@register.simple_tag
def replace_category(url, category):
    return re.sub(f'(category=)[^&]+', r'\1' + category.lower(), url)


@register.simple_tag
def multiply(qty, unit_price, *args, **kwargs):
    value = qty * unit_price
    try:
        value = int(value)
        return '{0:,}'.format(value).replace(',', ' ')
    except ValueError:
        return value
