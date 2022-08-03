from django.db import models

# Create your models here.

categories = [
    ('books', 'Книги'),
    ('electronics', 'Электроника'),
    ('pet_supplies', 'Зоотовары'),
    ('other', 'Разное')
]


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(max_length=2000, blank=True, verbose_name='Описание')
    category = models.CharField(choices=categories, default='other', max_length=12, verbose_name='Категория')
    available = models.PositiveIntegerField(verbose_name='В наличии')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return f'{self.id} {self.name} {self.category}'

    class Meta:
        db_table = 'products'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Cart(models.Model):
    product = models.ForeignKey('webapp.Product', on_delete=models.CASCADE, related_name='cart', verbose_name='Товар')
    count = models.PositiveIntegerField(verbose_name='Количество')

    def sum(self):
        return self.product.price * self.count

    def total(self):
        total = 0
        for i in Cart.objects.all():
            total += i.product.price * i.count
        return total

    class Meta:
        db_table = 'cart'
        verbose_name = 'В корзине'
