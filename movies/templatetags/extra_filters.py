# movies/templatetags/extra_filters.py

from django import template

register = template.Library()

@register.filter
def floatdiv(value, divisor):
    try:
        return float(value) / float(divisor)
    except (ValueError, ZeroDivisionError):
        return 0
