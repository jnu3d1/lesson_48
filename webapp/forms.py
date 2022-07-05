from django import forms
from django.forms import widgets

from webapp.models import categories


class ProductForm(forms.Form):
    name = forms.CharField(max_length=200, label='Наименование товара')
    description = forms.CharField(max_length=2000, label='Описание', required=False, widget=widgets.Textarea)
    category = forms.ChoiceField(choices=categories, label='Категория товаров')
    available = forms.IntegerField(min_value=0, label='В наличии')
    price = forms.DecimalField(max_digits=7, decimal_places=2, label='Цена')
