import ast
from django import template

register = template.Library()

@register.filter
def extract_keywords(keywords_str):
    try:
        keywords_list = ast.literal_eval(keywords_str)
        return ', '.join(next(iter(kw_set)) for kw_set in keywords_list)
    except:
        return ''