# Generated by Django 4.2 on 2023-04-13 02:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Productos', '0011_remove_products_nombre_producto'),
        ('Carrito', '0003_remove_cart_item_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart_item',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Productos.products'),
            preserve_default=False,
        ),
    ]