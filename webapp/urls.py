from django.urls import path

from webapp.views import *

urlpatterns = [
    path('', ProductsView.as_view(), name='index'),
    path('product/<int:pk>/', ProductView.as_view(), name='product_view'),
    path('products/add/', CreateProduct.as_view(), name='create'),
    path('product/<int:pk>/editing', UpdateProduct.as_view(), name='edit'),
    path('product/<int:pk>/delete/', DeleteProduct.as_view(), name='delete'),
    path('product/<int:pk>/cart_add/', cart_add, name='cart_add'),
    path('cart/', CartView.as_view(), name='cart'),
    # path('cart/<int:pk>/delete/', DeleteFromCart.as_view(), name='cart_delete'),
    path('cart/<int:pk>/delete/', delete_from_cart, name='cart_delete'),
]
