# Generated by Django 3.2.18 on 2023-06-25 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_initial'),
        ('users', '0004_auto_20230624_0719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to='orders.shippingaddress'),
        ),
    ]
