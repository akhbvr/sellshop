from django.contrib import admin

# Custom imports
from orders.models import (
    Order,
    OrderItem,
    ShippingAddress,
    WishList,
)

admin.site.register([OrderItem, ShippingAddress, WishList])

class OrderItemLine(admin.TabularInline):
    model = OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemLine]