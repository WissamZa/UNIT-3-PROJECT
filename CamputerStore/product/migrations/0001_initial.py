# Generated by Django 5.0.3 on 2024-04-09 02:01

import django.core.validators
import django.db.models.deletion
import product.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('model', models.CharField(max_length=200, unique=True)),
                ('category', models.CharField(choices=[('اجهزة الكمبيوتر', 'Pc'), ('اجهزة الكمبيوتر المحمول', 'Laptop'), ('قطع الكمبيوتر', 'Parts'), ('اكسسوارات', 'Accessories'), ('برامج', 'Software')], default='اجهزة الكمبيوتر', max_length=200)),
                ('price', models.FloatField()),
                ('discount', models.IntegerField(default=None, null=True)),
                ('in_stock', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=product.models.group_based_upload_to, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])])),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]
