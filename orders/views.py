from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from orders.models import WishList
from django.views.generic import ListView

class WishListView(ListView):
    template_name = "wishlist.html"
    model = WishList


    def get_queryset(self):
        return WishList.objects.filter(customer=self.request.user)