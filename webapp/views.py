from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.models import *
from webapp.forms import *


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
    queryset = Product.objects.filter(available__gt=0)
    template_name = 'product_view.html'


class CreateProduct(PermissionRequiredMixin, CreateView):
    form_class = ProductForm
    permission_required = 'webapp.add_product'
    template_name = 'create.html'

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class UpdateProduct(PermissionRequiredMixin, UpdateView):
    form_class = ProductForm
    model = Product
    permission_required = 'webapp.change_product'
    template_name = 'edit.html'

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class DeleteProduct(PermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = 'webapp.delete_product'
    template_name = 'delete.html'
    success_url = reverse_lazy('index')


def cart_add(request, pk):
    # product = Product.objects.get(pk=pk)
    # try:
    #     cart = Cart.objects.get(product=product)
    # except Cart.DoesNotExist:
    #     cart = None
    # if request.method == 'POST':
    #     if product.available > 0:
    #         if cart:
    #             cart.count += 1
    #             product.available -= 1
    #             product.save()
    #             cart.save()
    #         else:
    #             Cart.objects.create(product=product, count=1)
    #             product.available -= 1
    #             product.save()
    # return redirect('index')
    product = Product.objects.get(pk=pk)
    print(product)
    cart = request.session.get('cart', {})
    print(cart)
    if request.method == 'POST':
        count = int(request.POST.get('count'))
        print(count)
        if count > product.available:
            return HttpResponseBadRequest(f'К сожалению, мы таким количеством не располагаем.')
        else:
            if str(pk) in cart:
                cart[str(pk)] += count
            else:
                cart[str(pk)] = count
            request.session['cart'] = cart
        print(cart)
        print(request.session.get('cart'))
    next = request.GET.get('next')
    if next:
        return HttpResponseRedirect(next)
    return HttpResponseRedirect(reverse('index'))


class CartAdd(CreateView):
    model = Cart
    form_class = CartForm

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        count = form.cleaned_data.get('count')
        if count > product.available:
            return HttpResponseBadRequest(f'К сожалению, мы таким количеством не располагаем.')
        else:
            cart, created = Cart.objects.get_or_create(product=product, defaults={'count': count, })
            if not created:
                cart.count += count
                cart.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        next = self.request.GET.get('next')
        if next:
            return next
        return reverse('index')


class CartView(ListView):
    model = Cart
    template_name = 'cart.html'
    context_object_name = 'items'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['total'] = Cart.get_total()
        context['form'] = OrderForm()
        return context


class DeleteFromCart(DeleteView):
    model = Cart
    success_url = reverse_lazy('cart')

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.count -= 1
        if self.object.count < 1:
            self.object.delete()
        else:
            self.object.save()
        return HttpResponseRedirect(success_url)


def delete_from_cart(request, pk):
    cart = get_object_or_404(Cart, pk=pk)
    cart.product.available += cart.count
    cart.product.save()
    cart.delete()
    return redirect('cart')


class OrderCreate(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        order = form.save()
        # for item in Cart.objects.all():
        #     OrderedProducts.objects.create(product=item.product, order=order, quantity=item.count)
        #     item.product.available -= item.count
        #     item.product.save()
        #     # item.delete()
        # Cart.objects.all().delete()
        # return HttpResponseRedirect(self.success_url)

        products = []
        ordered_products = []

        for item in Cart.objects.all():
            ordered_products.append(OrderedProducts(product=item.product, quantity=item.count, order=order))
            item.product.available -= item.count
            products.append(item.product)

        OrderedProducts.objects.bulk_create(ordered_products)
        Product.objects.bulk_update(products, ('available',))
        Cart.objects.all().delete()
        return HttpResponseRedirect(self.success_url)