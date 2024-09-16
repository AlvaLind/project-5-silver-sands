# Generated by Django 5.1 on 2024-09-16 17:06

import cloudinary.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, unique=True)),
                ('description', models.TextField(blank=True, max_length=600, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Wine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('vintage', models.PositiveIntegerField()),
                ('volume', models.PositiveIntegerField()),
                ('closure', models.CharField(choices=[('natural cork', 'Natural Cork'), ('synthetic cork', 'Synthetic Cork'), ('agglomerate cork', 'Agglomerate Cork'), ('screw cap', 'Screw Cap'), ('champagne cork', 'Champagne Cork'), ('capped cork', 'Capped Cork')], max_length=20)),
                ('abv', models.DecimalField(decimal_places=2, max_digits=4)),
                ('acidity', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('residual_sugar', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('ph', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('stock', models.PositiveIntegerField()),
                ('image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('rating', models.FloatField(blank=True, null=True)),
                ('available', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wines', to='products.category')),
            ],
            options={
                'ordering': ['-vintage'],
            },
        ),
    ]
