from django import template

register = template.Library()


@register.filter
def lookup(d, key):
    return d.get(key)


@register.filter
def string_formatting(string):

    return string[1:-1]


@register.filter
def modulo(num, val):
    return num % val


@register.filter
def get_range(val):
    return xrange(val)
