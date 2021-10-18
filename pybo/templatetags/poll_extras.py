import re
from django import template

register = template.Library()

@register.filter
def add_page(value, arg):
    if arg == None:
        return value
    return value + 'page=' + str(arg) + '&'

@register.filter
def add_query(value, arg):
    if arg == None:
        return value
    return value + 'query=' + arg + '&'

@register.filter
def add_type(value, arg):
    if arg == None:
        return value
    return value + 'type=' + arg + '&'

@register.filter
def convert_html_to_text(value):
    # *, +, ? => 최대 매칭
    # 최대 매칭되는 한정자 뒤에 ?를 붙여주면 최소 매칭
    convert_string = re.sub(r'<.*?>', '', value)
    return convert_string
