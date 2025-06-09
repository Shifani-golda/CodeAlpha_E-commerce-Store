from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def calc_order_total(order_items):
    total = 0
    for item in order_items:
        total += item.price * item.quantity
    return total

