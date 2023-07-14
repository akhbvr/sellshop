from django.db import models

# Custom imports
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
User = get_user_model()


class Category(models.Model):
    name = models.CharField(verbose_name='Category name', max_length=50, db_index=True)

    parent = models.ForeignKey('self', verbose_name='Parent comment', on_delete=models.CASCADE, related_name='parent_category', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(verbose_name='Brand name', max_length=50, db_index=True)
    image = models.ImageField(verbose_name='Brand image', upload_to='products/brand')
    description = models.TextField(verbose_name='Description')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(verbose_name='Tag name', max_length=50, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Attribute(models.Model):
    name = models.CharField(verbose_name='Attribute name', max_length=50, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Attribute'
        verbose_name_plural = 'Attributes'

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    value = models.CharField(verbose_name='Attribute value', max_length=50, db_index=True)

    attribute = models.ForeignKey(Attribute, verbose_name='Attribute', on_delete=models.CASCADE, related_name='attributevalue_attribute')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Attribute Value'
        verbose_name_plural = 'Attribute Values'

    def __str__(self):
        return self.value


class Discount(models.Model):
    DISCOUNT_TYPE_CHOICES = (
    (1, 'Percent'),
    (2, 'Unit'),
    )
    discount_type = models.IntegerField(verbose_name='Discount type', choices=DISCOUNT_TYPE_CHOICES, null=True, blank=True)
    discount_amount = models.FloatField(verbose_name='Discount amount', default=0.00)
    discount_start_time = models.DateTimeField(verbose_name='Discount start time', auto_now_add=False, null=True, blank=True)
    discount_end_time = models.DateTimeField(verbose_name='Discount end time', auto_now_add=False, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Discount'
        verbose_name_plural = 'Discounts'

    def __str__(self):
        return f"{self.discount_start_time}"


class Product(models.Model):
    name = models.CharField(verbose_name='Product name', max_length=150, db_index=True)
    is_active = models.BooleanField(verbose_name='Is active', default=True)

    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.CASCADE, related_name='product_category')
    brand = models.ForeignKey(Brand, verbose_name='Brand', on_delete=models.CASCADE, related_name='product_brand')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name


class ProductVariation(models.Model):
    sku = models.IntegerField(verbose_name='product code')
    main_image = models.ImageField(verbose_name='Main image', upload_to='products/product_variations')
    price = models.FloatField(verbose_name='Price')
    stock = models.IntegerField(verbose_name='Stock')
    stock_status = models.BooleanField(verbose_name='Stock status')
    short_desctiption = models.CharField(verbose_name='Short description', max_length=50)
    description = models.TextField(verbose_name='Description')
    avg_rating = models.FloatField(verbose_name='AVG rating', default=0.00)
    is_active = models.BooleanField(verbose_name='Is active', default=True)
    slug = models.SlugField(null=True, blank=True, unique=True, editable=False)

    product = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE, related_name='productvariation_product')
    product_attribute_values = models.ManyToManyField(AttributeValue, verbose_name='Attribute value', related_name='productvariation_attribute_value')
    product_tags = models.ManyToManyField(Tag, verbose_name='Tag', related_name='productvariation_tag')
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product Variation'
        verbose_name_plural = 'Product Variations'

    def __str__(self):
        return self.product.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product.name) + slugify(self.sku)
        return super().save(*args, **kwargs)


class ProductImage(models.Model):
    image = models.ImageField(verbose_name='Image', upload_to='products/products_variations')

    product_variation = models.ForeignKey(ProductVariation, verbose_name='Product variation', on_delete=models.CASCADE, related_name='productimage_productvariation')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'

    def __str__(self):
        return self.product_variation.product.name


class Review(models.Model):
    STAR_CHOICES = (
        (1, '*'),
        (2, '**'),
        (3, '***'),
        (4, '****'),
        (5, '*****'),
    )
    rating = models.IntegerField(verbose_name='Rating', null=True, blank=True, choices=STAR_CHOICES, default=1)
    comment = models.TextField(verbose_name='Comment')

    product_variation = models.ForeignKey(ProductVariation, verbose_name='Product varitaion', on_delete=models.CASCADE, related_name='review')
    customer = models.ForeignKey(User, verbose_name='Customer', on_delete=models.CASCADE, related_name='review_customer')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.product_variation.product.name