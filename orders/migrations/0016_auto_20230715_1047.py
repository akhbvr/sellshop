# Generated by Django 3.2.18 on 2023-07-15 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_auto_20230715_1037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_item',
        ),
        migrations.AddField(
            model_name='order',
            name='order_item',
            field=models.ManyToManyField(related_name='orderitem_order', to='orders.OrderItem', verbose_name='Order item'),
        ),
    ]