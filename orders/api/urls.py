from django.urls import path
from orders.api.views import (
    ProductVariationAPIView,
    ProductVariationRetrieveUpdateDestroyAPIView,
    WishListAPIView,
    BrandListAPIView,
    WishListRetrieveUpdateDestroyAPIView,
    attributes,
    BasketAPIView,
    BasketRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path('products/', ProductVariationAPIView.as_view(), name="products"),
    path('products/<int:pk>/', ProductVariationRetrieveUpdateDestroyAPIView.as_view(), name="product_read_update_delete"),

    path('wishlist/', WishListAPIView.as_view(), name="wishlist"),
    path('wishlist/<int:pk>/<int:p_k>/', WishListRetrieveUpdateDestroyAPIView.as_view(), name="wishlist_read_update_delete"),

    path('basket/', BasketAPIView.as_view(), name="basket"),
    path('basket/<int:pk>/', BasketRetrieveUpdateDestroyAPIView.as_view(), name="basket_read_update_delete"),

    path('brands/', BrandListAPIView.as_view(), name="brands"),

    path('attributes/', attributes, name="attributes")
]
