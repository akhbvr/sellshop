# Generated by Django 3.2.18 on 2023-07-14 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_productvariation_slug'),
        ('orders', '0008_alter_wishlist_product_variation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='product_variation',
        ),
        migrations.AddField(
            model_name='wishlist',
            name='product_variation',
            field=models.ManyToManyField(related_name='wishlist_product_variation', to='products.ProductVariation', verbose_name='Product variation'),
        ),
    ]
