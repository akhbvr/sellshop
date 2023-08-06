from django.urls import path
from orders.views import WishListView, CartView

app_name = 'orders'

urlpatterns = [
    path('wishlist', WishListView.as_view(), name="wishlist"),
    path('cart', CartView.as_view(), name="cart"),
]
