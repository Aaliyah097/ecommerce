from django import template
import re

register = template.Library()


@register.simple_tag
def replace_category(url, category):
    return re.sub(f'(category=)[^&]+', r'\1' + category.lower(), url)
