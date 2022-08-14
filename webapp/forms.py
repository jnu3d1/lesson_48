from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from webapp.models import Product, Cart, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'available', 'price']
        widgets = {
            'description': widgets.Textarea,
        }

    def clean_available(self):
        available = self.cleaned_data.get('available')
        if available < 0:
            raise ValidationError('Значение не должно быть отрицательным!')
        return available


class SearchForm(forms.Form):
    search = forms.CharField(label='Поиск', max_length=50, required=False)


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['count']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'phone_number', 'address']
