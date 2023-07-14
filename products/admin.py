from django.contrib import admin

# Custom imports
from products.models import (
    Category,
    Brand,
    Tag,
    Attribute,
    AttributeValue,
    Discount,
    Product,
    ProductVariation,
    ProductImage,
    Review,
)

admin.site.register([
    Category,
    Brand,
    Tag,
    Attribute,
    AttributeValue,
    Discount,
    Product,
    ProductImage,
    Review,
])


class ProductVariationImageLine(admin.TabularInline):
    model = ProductImage

@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    inlines = [ProductVariationImageLine]