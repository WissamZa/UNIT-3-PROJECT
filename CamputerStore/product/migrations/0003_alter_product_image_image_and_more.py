# Generated by Django 5.0.3 on 2024-04-14 14:27

import django.core.validators
import django.db.models.deletion
import product.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_rename_productimage_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_image',
            name='image',
            field=models.ImageField(upload_to=product.models.group_based_upload_to, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])], verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='product_image',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Images', to='product.product'),
        ),
    ]