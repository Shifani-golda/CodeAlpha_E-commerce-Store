# Generated by Django 5.2.1 on 2025-05-30 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_product_key_ingredients_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='benefits',
            field=models.TextField(default=''),
        ),
    ]
