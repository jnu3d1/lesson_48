from django.http import HttpResponseNotFound
from django.shortcuts import render

# Create your views here.

from webapp.models import Product


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
