from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.models import Product, Cart
from webapp.forms import ProductForm, SearchForm, CartForm


class ProductsView(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        self.form = SearchForm(self.request.GET)
        if self.form.is_valid():
            self.search_value = self.form.cleaned_data.get('search')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Product.objects.filter(name__icontains=self.search_value)
        return super().get_queryset().order_by('category', 'name').filter(available__gt=0)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            query = urlencode({'search': self.search_value})
            context['query'] = query
            context['search'] = self.search_value
        return context


class ProductView(DetailView):
    model = Product
    template_name = 'product_view.html'


class CreateProduct(CreateView):
    form_class = ProductForm
    template_name = 'create.html'

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class UpdateProduct(UpdateView):
    form_class = ProductForm
    model = Product
    template_name = 'edit.html'

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class DeleteProduct(DeleteView):
    model = Product
    template_name = 'delete.html'
    success_url = reverse_lazy('index')


def cart_add(request, pk):
    product = Product.objects.get(pk=pk)
    try:
        cart = Cart.objects.get(product=product)
    except Cart.DoesNotExist:
        cart = None
    if request.method == 'POST':
        if product.available > 0:
            if cart:
                cart.count += 1
                product.available -= 1
                product.save()
                cart.save()
            else:
                Cart.objects.create(product=product, count=1)
                product.available -= 1
                product.save()
    return redirect('index')


class CartAdd(CreateView):
    model = Cart
    form_class = CartForm

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        count = form.cleaned_data.get('count')
        print(count)
        if count > product.available:
            pass
        else:
            cart, is_created = Cart.objects.get_or_create(product=product, defaults={'count': 1, })
            print(cart, is_created)
            if is_created:
                cart.count = count
            else:
                cart.count += count
            cart.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('index')


class CartView(ListView):
    model = Cart
    template_name = 'cart.html'
    context_object_name = 'items'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['total'] = Cart.get_total()
        return context


class DeleteFromCart(DeleteView):
    model = Cart
    success_url = reverse_lazy('cart')


def delete_from_cart(request, pk):
    cart = get_object_or_404(Cart, pk=pk)
    cart.product.available += cart.count
    cart.product.save()
    cart.delete()
    return redirect('cart')
