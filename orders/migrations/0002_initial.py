# Generated by Django 3.2.18 on 2023-06-24 07:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='product_variation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist_product_variation', to='products.productvariation', verbose_name='Product variation'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderitem_order', to='orders.order', verbose_name='Order'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product_variation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderitem_product_variation', to='products.productvariation', verbose_name='Product variation'),
        ),
    ]
