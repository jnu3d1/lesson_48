from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

from webapp.models import Product
from webapp.forms import ProductForm


def index(request):
    if request.method == 'GET':
        products = Product.objects.filter(available__gt=0).order_by('category', 'name')
        return render(request, 'index.html', {'products': products})
    else:
        name = request.POST.get('name')
        products = Product.objects.filter(name=name)
        return render(request, 'index.html', {'products': products, 'name': name})


def product_view(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return HttpResponseNotFound('<h1>Страница не найдена</h1>')
    return render(request, 'product_view.html', {'product': product})


def create_product(request):
    if request.method == 'GET':
        product = ProductForm()
        return render(request, 'create.html', {'product': product})
    else:
        product = ProductForm(data=request.POST)
        if product.is_valid():
            name = product.cleaned_data.get('name')
            description = product.cleaned_data.get('description')
            category = product.cleaned_data.get('category')
            available = product.cleaned_data.get('available')
            price = product.cleaned_data.get('price')
            Product.objects.create(name=name, description=description, category=category, available=available,
                                   price=price)
            return redirect('index')
        return render(request, 'create.html', {'product': product})


def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        return render(request, 'edit.html', {'product': product})
    else:
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.category = request.POST.get('category')
        product.available = request.POST.get('available')
        product.price = request.POST.get('price')
        product.save()
        return redirect('product_view', pk=product.pk)


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        return render(request, 'delete.html', {'product': product})
    product.delete()
    return redirect('index')
