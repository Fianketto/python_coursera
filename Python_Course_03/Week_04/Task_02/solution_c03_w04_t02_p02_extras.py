from django import template

register = template.Library()


@register.filter(name='inc')
def inc(a, b):
    return str(int(a) + int(b))


@register.simple_tag
def division(a, b, to_int=False):
    c = float(a)/float(b)
    if to_int:
        c = int(c)
    return str(c)
