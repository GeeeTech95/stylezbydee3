from django import template
from shop.models import Product
register = template.Library()


@register.filter
def product_attribute_values(product, attribute_pk):
    # gets all values for the attribute of a particular product as a list
    # attrute is a pk of attribute field
    return product.product_attribute_values(attribute_pk)


@register.filter
def trending_products(gender, count=None):
    results = Product.trending.filter(gender=gender)
    if count and count is int and count > 0:
        return results[:count]
    return results
