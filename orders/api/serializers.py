from rest_framework import serializers
from products.models import ProductVariation, AttributeValue, Attribute, Product, Brand
from orders.models import WishList, Order, OrderItem
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = (
            "name",
        )


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer()
    class Meta:
        model = AttributeValue
        fields = (
            "attribute",
            "value",
        )

    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "name",
        )


class ProductVariationSerializer(serializers.ModelSerializer):
    product_attribute_values = ProductAttributeValueSerializer(many=True)
    product = ProductSerializer()
    class Meta:
        model = ProductVariation
        fields = (
            "id",
            "sku",
            "main_image",
            "price",
            "stock",
            "stock_status",
            "short_desctiption",
            "description",
            "avg_rating",
            "is_active",
            "slug",
            "product",
            "discount",
            "product_attribute_values",
            "product_tags",
        )


class ProductVariationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariation
        fields = (
            "id",
            "slug",
            "sku",
            "main_image",
            "price",
            "stock",
            "stock_status",
            "short_desctiption",
            "description",
            "avg_rating",
            "is_active",
            "product",
            "discount",
            "product_attribute_values",
            "product_tags",
        )

    
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
        )


class WishListSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    class Meta:
        model = WishList
        fields = (
            "id",
            "product_variation",
            "customer",
        )


class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            'quantity',
            'product_variation',
            'order',
        )


class OrderItemSerializer(serializers.ModelSerializer):
    product_variation = ProductVariationSerializer()
    class Meta:
        model = OrderItem
        fields = (
            'id',
            'quantity',
            'total_amount',
            'product_variation',
            'order',
        )


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    product_variation = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = (
            'status',
            'customer',
            'product_variation',
        )
    def get_product_variation(self, obj):
        serializer = OrderItemSerializer(obj.orderitem_order.all(), context=self.context ,many=True)
        return serializer.data


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'status',
            'customer',
        )


class WishListCreateSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(read_only=True)
    product_variation = serializers.PrimaryKeyRelatedField(queryset=ProductVariation.objects.all(), many=True)
    
    class Meta:
        model = WishList
        fields = (
            "id",
            "product_variation",
            "customer",
        )

    def validate(self, attrs):
        request = self.context['request']
        attrs['customer'] = request.user
        return super().validate(attrs)
    

class UserTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        serializer = CustomerSerializer(user)
        data.update(serializer.data)
        return data


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            "id",
            "name",
            "image",
        )