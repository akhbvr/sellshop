# Generated by Django 3.2.18 on 2023-07-09 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_productvariation_slug'),
        ('orders', '0006_alter_wishlist_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='product_variation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist_product_variation', to='products.productvariation', unique=True, verbose_name='Product variation'),
        ),
    ]