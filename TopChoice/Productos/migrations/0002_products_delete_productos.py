# Generated by Django 4.1 on 2023-03-01 03:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Categorias', '0002_subcategory'),
        ('Productos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('product_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('product_name', models.CharField(max_length=50)),
                ('slug', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('product_image_stock', models.ImageField(upload_to='photos/products/stock')),
                ('product_image_secundary', models.ImageField(upload_to='photos/products/secundary')),
                ('product_image_extra', models.ImageField(upload_to='photos/products/extra')),
                ('stock', models.IntegerField()),
                ('is_available', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Categorias.category')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Categorias.subcategory')),
            ],
        ),
        migrations.DeleteModel(
            name='Productos',
        ),
    ]
