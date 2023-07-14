from django.db import models

# Custom imports
from products.models import ProductVariation
from django_countries.fields import CountryField
from django.contrib.auth import get_user_model
User = get_user_model()


class Order(models.Model):
    status = models.BooleanField(verbose_name='Status', default=False)
    total_amount = models.FloatField(verbose_name='Total amount')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return self.status


class OrderItem(models.Model):
    quantity = models.IntegerField(verbose_name='Quantity')
    price = models.FloatField(verbose_name='Price')

    order = models.ForeignKey(Order, verbose_name='Order', on_delete=models.CASCADE, related_name='orderitem_order')
    product_variation = models.ForeignKey(ProductVariation, verbose_name='Product variation', on_delete=models.CASCADE, related_name='orderitem_product_variation')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return self.product_variation.product.name


class ShippingAddress(models.Model):
    line_1 = models.CharField(verbose_name='Line 1', max_length=255)
    line_2 = models.CharField(verbose_name='Line 2', max_length=255)
    address = models.CharField(verbose_name='Address', max_length=255)
    postal_code = models.CharField(verbose_name='Postal code', max_length=50)
    country = CountryField(verbose_name='Country')
    city = models.CharField(verbose_name='City', max_length=100)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Shipping Address'
        verbose_name_plural = 'Shipping Addresses'

    def __str__(self):
        return self.postal_code


class WishList(models.Model):
    product_variation = models.ManyToManyField(ProductVariation, verbose_name='Product variation', related_name='wishlist_product_variation')
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Wish List'
        verbose_name_plural = 'Wish Lists'

    def __str__(self):
        return f"{self.customer.username}"
    
    