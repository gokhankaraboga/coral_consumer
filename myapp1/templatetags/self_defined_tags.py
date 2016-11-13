from django import template

register = template.Library()


@register.filter
def lookup(d, key):
    return d.get(key)


@register.filter
def modulo(num, val):
    return num % val
