# Generated by Django 3.2.18 on 2023-06-27 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_category_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='review',
            name='product_variation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='products.productvariation', verbose_name='Product varitaion'),
        ),
    ]
