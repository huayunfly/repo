"""
Definition of custom filter
"""

from django import template

register = template.Library()


@register.filter
def lookup(d, key):
    """Get a value according to the key or an item indexing"""
    return d[key]
