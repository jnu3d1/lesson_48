# Generated by Django 4.0.6 on 2022-08-13 04:51

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('phone_number', models.CharField(max_length=30, verbose_name='Номер телефона')),
                ('address', models.CharField(max_length=100, verbose_name='Адрес')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'db_table': 'orders',
            },
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=7, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена'),
        ),
        migrations.CreateModel(
            name='OrderedProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordered_products', to='webapp.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordered_products', to='webapp.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Заказанный товар',
                'verbose_name_plural': 'Заказанные товары',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='orders', through='webapp.OrderedProducts', to='webapp.product', verbose_name='Товары'),
        ),
    ]
