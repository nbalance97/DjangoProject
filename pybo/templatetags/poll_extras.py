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
