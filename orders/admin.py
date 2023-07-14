from django.contrib import admin

# Custom imports
from orders.models import (
    Order,
    OrderItem,
    ShippingAddress,
    WishList,
)

admin.site.register([Order, OrderItem, ShippingAddress, WishList])