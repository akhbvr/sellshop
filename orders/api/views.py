from django.http import JsonResponse
from products.models import ProductVariation, Attribute, Brand
from orders.models import WishList, Order, OrderItem
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from orders.api.serializers import (
    ProductVariationSerializer,
    AttributeSerializer,
    ProductVariationCreateSerializer,
    WishListSerializer,
    WishListCreateSerializer,
    BrandSerializer,
    OrderCreateSerializer,
    OrderSerializer,
    OrderItemCreateSerializer,
)
from rest_framework.decorators import api_view
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)


class BasketAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderCreateSerializer

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)
    

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderCreateSerializer
        return OrderSerializer
    
    def post(self, request, format=None):

        def create_order_item(order):
                order_item_data = {
                    "quantity": int(request.data.get("quantity", 1)),
                    "product_variation": int(request.data.get("product_variation")),
                    "order": order
                }
                if not OrderItem.objects.filter(order__id=order, product_variation=order_item_data.get("product_variation")).exists():
                    order_item_serializer = OrderItemCreateSerializer(data=order_item_data)
                    if order_item_serializer.is_valid():
                        order_item_serializer.save()
                        return Response(order_item_serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        return Response(order_item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(data={"message": "This product is already available."}, status=status.HTTP_409_CONFLICT)

        if not Order.objects.filter(customer=request.user).exists():
            order_data = {
                'status': True,
                'customer': request.user.id
            }
            order_serializer = OrderCreateSerializer(data=order_data)
            if order_serializer.is_valid():
                order = order_serializer.save()
                return create_order_item(order.id)
            else:
                return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif Order.objects.filter(customer=request.user).exists():
            order_id = Order.objects.get(customer=request.user).id
            return create_order_item(order_id)


class BasketRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Order
    serializer_class = OrderCreateSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return OrderSerializer
        return super().get_serializer_class()
    
    def destroy(self, request, *args, **kwargs):

        try:
            order = Order.objects.get(customer=self.request.user)
            product_variation = ProductVariation.objects.get(id=kwargs.get("pk"))
            order_item = OrderItem.objects.get(order=order, product_variation=product_variation)
            order_item.delete()
            return Response(data={"message": "Product removed from basket successfully."}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={"message": "Product not found or an error occured."}, status=status.HTTP_409_CONFLICT)


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
    serializer_class = WishListCreateSerializer

    def get_queryset(self):
        return WishList.objects.filter(customer=self.request.user)
    

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




