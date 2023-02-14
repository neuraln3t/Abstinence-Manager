from django import template

register = template.Library()

@register.filter(name="split")
def split(value, key):
    if type(value) != str:
        value = str(value)

    return value.split(key)[0]