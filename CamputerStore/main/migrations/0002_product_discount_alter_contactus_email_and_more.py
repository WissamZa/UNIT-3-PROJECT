# Generated by Django 5.0.3 on 2024-04-07 14:07

import main.validator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='email',
            field=models.EmailField(max_length=254, validators=[main.validator.validate_email]),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='phone',
            field=models.CharField(max_length=10, validators=[main.validator.validate_phone]),
        ),
    ]
