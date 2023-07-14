from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product, ProductVariation, Category, Attribute, Brand
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin
from products.forms import CommentForm
from django.urls import reverse_lazy
from django.db.models import Avg
from urllib.parse import urlencode


class ProductsView(ListView):
    model = ProductVariation
    template_name = 'product-list.html'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        brand_id = self.request.GET.get('brand_id')
        category_id = self.request.GET.get('category_id')
        sub_category_id = self.request.GET.get('sub_category_id')
        if brand_id:
            queryset = queryset.filter(product__brand__id=brand_id)

        if category_id:
            queryset = queryset.filter(product__category__id=category_id)

        if sub_category_id:
            queryset = queryset.filter(product__category__id=sub_category_id)
            
        for attribute in Attribute.objects.all():
            attribute_name = attribute.name.lower()
            attribute_value_id = self.request.GET.get(f'{attribute_name}_id')
            if attribute_value_id:
                queryset = queryset.filter(product_attribute_values__id=attribute_value_id)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['attributes'] = Attribute.objects.all()
        context['brands'] = Brand.objects.all()

        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        context['query_params'] = urlencode(query_params)
        return context


class SingleProduct(FormMixin, DetailView):
    form_class = CommentForm
    model = ProductVariation
    template_name = 'single-product.html'

    def get_success_url(self):
        return reverse_lazy("products:single_product", kwargs={"slug": self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = ProductVariation.objects.all().order_by("-created_at")[:4]
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form):
        form.instance.product_variation = self.get_object()
        form.instance.customer = self.request.user
        form.save()
        avg_rating = self.object.review.all().aggregate(Avg('rating'))
        self.object.avg_rating = round(avg_rating.get('rating__avg'), 2)
        self.object.save()
        return super().form_valid(form)



