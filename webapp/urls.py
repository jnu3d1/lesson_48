from django.urls import path

from webapp.views import *

urlpatterns = [
    path('', ProductsView.as_view(), name='index'),
    path('product/<int:pk>/', ProductView.as_view(), name='product_view'),
    path('products/add/', CreateProduct.as_view(), name='create'),
    path('product/<int:pk>/editing', UpdateProduct.as_view(), name='edit'),
    path('product/<int:pk>/delete/', DeleteProduct.as_view(), name='delete'),
]
