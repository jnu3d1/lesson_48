from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.models import Product
from webapp.forms import ProductForm, SearchForm


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
    template_name = 'create.html'

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class DeleteProduct(DeleteView):
    model = Product
    template_name = 'delete.html'
    success_url = reverse_lazy('index')
