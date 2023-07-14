from django.http import JsonResponse
from products.models import ProductVariation, Attribute, Brand
from orders.models import WishList
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from orders.api.serializers import (
    ProductVariationSerializer,
    AttributeSerializer,
    ProductVariationCreateSerializer,
    WishListSerializer,
    WishListCreateSerializer,
    BrandSerializer
)
from rest_framework.decorators import api_view
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)


class WishListRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = WishList.objects.all()
    serializer_class = WishListCreateSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return WishListSerializer
        return super().get_serializer_class()
    
    def destroy(self, request, *args, **kwargs):
        
        def get_object(self):
            super().get_object()
            return WishList.objects.get(id=kwargs.get("pk"))
        
        instance = get_object(self)
        print("\n\n\n\n\n\n", instance, "\n\n\n\n\n\n")
        product_variation_id = kwargs.get('p_k')
        instance.product_variation.remove(product_variation_id)
        return Response(data={"message": "Product removed from wishlist successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response(data={"message": "Product deleted successfully in the wishlist."}, status=status.HTTP_204_NO_CONTENT)


class ProductVariationAPIView(ListCreateAPIView):
    queryset = ProductVariation.objects.all()
    serializer_class = ProductVariationCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductVariationCreateSerializer
        return ProductVariationSerializer
    

class ProductVariationRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ProductVariation.objects.all()
    serializer_class = ProductVariationCreateSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductVariationSerializer
        return super().get_serializer_class()
    
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(data={'message': 'Product deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class WishListAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = WishList.objects.all()
    serializer_class = WishListCreateSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return WishListCreateSerializer
        return WishListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_variation_ids = serializer.validated_data.get('product_variation', [])
        customer = request.user

        try:
            wishlist = WishList.objects.get(customer=customer)
        except WishList.DoesNotExist:
            wishlist = WishList.objects.create(customer=customer)

        wishlist.product_variation.add(*product_variation_ids)

        return Response(
            data={"message": "Product added to wishlist successfully."},
            status=status.HTTP_201_CREATED
        )


class BrandListAPIView(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer






















# @api_view(http_method_names=['GET', 'POST'])
# def products(request):
#     if request.method == "POST":
#         serializer = ProductVariationCreateSerializer(data=request.data, context={"request": request})
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(data=serializer.data, status=201, safe=False)
#         return JsonResponse(data=serializer.errors, status=400, safe=False)
    
#     product_variation = ProductVariation.objects.all()
#     serializer = ProductVariationSerializer(instance=product_variation, many=True, context={"request": request})
#     return JsonResponse(data=serializer.data, safe=False)


# @api_view(http_method_names=['PUT', 'PATCH', 'DELETE'])
# def product_read_update_delete(request, pk):
#     if request.method == "PUT":
#         product = ProductVariation.objects.get(id=pk)
#         serializer = ProductVariationCreateSerializer(data=request.data, instance=product, context={"request": request})
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(data=serializer.data, status=200, safe=False)
#         return JsonResponse(data=serializer.errors, status=400, safe=False)
    
#     if request.method == "PATCH":
#         product = ProductVariation.objects.get(id=pk)
#         serializer = ProductVariationCreateSerializer(data=request.data, instance=product, partial=True, context={"request": request})
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(data=serializer.data, status=200, safe=False)
#         return JsonResponse(data=serializer.errors, status=400, safe=False)

#     if request.method == "DELETE":
#         product = ProductVariation.objects.get(id=pk)
#         product.delete()
#         return JsonResponse(data={'message': 'Product deleted successfully.'}, status=204)




@api_view(http_method_names=['GET', 'POST'])
def attributes(request):
    if request.method == "POST":
        data = request.POST
        serializer = AttributeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(data=serializer.data, status=201, safe=False)
        
        return JsonResponse(data=serializer.errors, status=400, safe=False)
    
    attributes = Attribute.objects.all()
    serializer = AttributeSerializer(instance=attributes ,many=True)
    return JsonResponse(data=serializer.data, safe=False)




