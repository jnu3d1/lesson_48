from django.urls import path

from webapp.views import index, product_view, create_product, edit_product, delete_product

urlpatterns = [
    path('', index, name='index'),
    path('product/<int:pk>/', product_view, name='product_view'),
    path('products/add/', create_product, name='create'),
    path('task/<int:pk>/editing', edit_product, name='edit'),
    path('task/<int:pk>/delete/', delete_product, name='delete'),
]
