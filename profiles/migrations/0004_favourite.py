# Generated by Django 5.1 on 2024-10-06 14:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_wine_sku'),
        ('profiles', '0003_alter_userprofile_default_phone_number'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Favourite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourited_by', to=settings.AUTH_USER_MODEL)),
                ('wine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to='products.wine')),
            ],
            options={
                'unique_together': {('user', 'wine')},
            },
        ),
    ]
