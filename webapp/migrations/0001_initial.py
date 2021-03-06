# Generated by Django 4.0.6 on 2022-07-05 08:35

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
                ('name', models.CharField(max_length=100, verbose_name='Наименование')),
                ('description', models.TextField(blank=True, max_length=2000, verbose_name='Описание')),
                ('category', models.CharField(choices=[('books', 'Книги'), ('electronics', 'Электроника'), ('pet_supplies', 'Зоотовары'), ('other', 'Разное')], default='other', max_length=12, verbose_name='Категория')),
                ('available', models.PositiveIntegerField(verbose_name='В наличии')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'db_table': 'products',
            },
        ),
    ]
