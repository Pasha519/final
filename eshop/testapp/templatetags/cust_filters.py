from django import template
register = template.Library()

@register.filter(name='currency')
def price_filter(value):
    result = "Rs."+str(value)
    return result