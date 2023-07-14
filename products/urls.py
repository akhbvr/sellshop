from django.urls import path
from products.views import ProductsView, SingleProduct

app_name = 'products'

urlpatterns = [
    path('', ProductsView.as_view(), name="product_list"),
    path('<slug:slug>', SingleProduct.as_view(), name="single_product"),
]
