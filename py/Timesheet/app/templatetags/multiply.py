"""
Definition of custom filter
"""

from django import template

register = template.Library()


@register.filter
def multiply(lhs, factor):
    """Multiply a value with the factor.
    @param lhs: the original value
    @param factor: the multiplier
    @return the product if it is successful. otherwise None.
    """
    try:
        return float(lhs) * float(factor)
    except ValueError:
        return None
