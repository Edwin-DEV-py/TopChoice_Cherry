# Generated by Django 4.2 on 2023-04-08 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Productos', '0006_alter_products_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='description',
            field=models.CharField(max_length=300),
        ),
    ]
