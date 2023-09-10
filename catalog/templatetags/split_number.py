from django import template

register = template.Library()


@register.filter
def split_number(value):
    print(value)
    try:
        value = int(value)
        return '{0:,}'.format(value).replace(',', ' ')
    except ValueError:
        return value
