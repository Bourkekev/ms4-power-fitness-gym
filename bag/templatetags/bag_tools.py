from django import template


register = template.Library()


@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    """ calc_subtotal:

    * Calculates the line item subtotal

    \n Args:
    1. price: item price
    2. quantity: quantity of the item

    \n Returns:
    * price times the quantity
    """
    return price * quantity
