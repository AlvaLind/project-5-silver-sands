# Generated by Django 5.1 on 2024-10-10 13:17

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_remove_wine_ph'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wine',
            name='price',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=6),
        ),
    ]
