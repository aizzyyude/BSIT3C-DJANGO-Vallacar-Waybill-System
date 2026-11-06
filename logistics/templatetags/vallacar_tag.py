
from django import template

register = template.Library()

@register.filter
def get_field(record, field_name):
    value = getattr(record, field_name, "")
    return value if value is not None else "-"
