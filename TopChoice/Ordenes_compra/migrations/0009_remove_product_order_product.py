# Generated by Django 4.2 on 2023-04-13 02:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ordenes_compra', '0008_payment_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product_order',
            name='product',
        ),
    ]
