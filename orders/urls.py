from django.urls import path
from orders.views import WishListView

app_name = 'orders'

urlpatterns = [
    path('wishlist', WishListView.as_view(), name="wishlist"),
]
