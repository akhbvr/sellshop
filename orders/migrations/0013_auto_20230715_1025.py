# Generated by Django 3.2.18 on 2023-07-15 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_productvariation_slug'),
        ('orders', '0012_alter_orderitem_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='product_variation',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product_variation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orderitem_product_variation', to='products.productvariation', verbose_name='Product variation'),
        ),
    ]
