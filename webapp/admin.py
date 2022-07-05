from django.contrib import admin

from webapp.models import Product


# Register your models here.

class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_display_links = ['name']
    list_filter = ['category']
    search_fields = ['name']
    fields = ['name', 'description', 'category', 'available', 'price']


admin.site.register(Product, ProductsAdmin)
