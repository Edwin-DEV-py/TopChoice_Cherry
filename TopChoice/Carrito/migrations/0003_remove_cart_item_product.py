# Generated by Django 4.2 on 2023-04-13 02:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Carrito', '0002_alter_cart_cart_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart_item',
            name='product',
        ),
    ]
