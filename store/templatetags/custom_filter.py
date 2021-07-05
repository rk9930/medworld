from django import template

register = template.Library()
# filter to check whether the product is added in cart or not!!!!!.

@register.filter(name='currency')
def currency(number):
    return "₹" + str(number)

@register.filter(name='multiply')
def multiply(number1, number2):
    return number1 * number2
