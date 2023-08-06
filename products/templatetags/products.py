from django import template
from orders.models import WishList, OrderItem

register = template.Library()

@register.simple_tag(name='is_product_in_wishlist')
def is_product_in_wishlist(product, user):
    return product.wishlist_product_variation.filter(customer=user).exists()


@register.simple_tag(name="get_wishlist_id")
def get_wishlist_id(user):
    return WishList.objects.get(customer=user).id


@register.simple_tag(name="check_basket")
def check_basket(product, user):
    return product.orderitem_product_variation.filter(order__customer=user).exists()