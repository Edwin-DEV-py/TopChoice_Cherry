# Generated by Django 4.2 on 2023-04-15 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuario', '0010_profile_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='img',
            field=models.ImageField(blank=True, upload_to='profile_img'),
        ),
    ]
