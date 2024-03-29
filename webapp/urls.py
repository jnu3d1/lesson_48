from django.urls import path

from webapp.views import *

urlpatterns = [
    path('', ProductsView.as_view(), name='index'),
    path('product/<int:pk>/', ProductView.as_view(), name='product_view'),
    path('products/add/', CreateProduct.as_view(), name='create'),
    path('product/<int:pk>/editing', UpdateProduct.as_view(), name='edit'),
    path('product/<int:pk>/delete/', DeleteProduct.as_view(), name='delete'),
    path('product/<int:pk>/add_to_cart/', cart_add, name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/<int:pk>/delete/', DeleteFromCart.as_view(), name='cart_delete'),
    # path('cart/<int:pk>/delete/', delete_from_cart, name='cart_delete'),
    # path('product/<int:pk>/add_to_cart/', CartAdd.as_view(), name='add_to_cart'),
    path('order/create/', OrderCreate.as_view(), name='create_order'),
]
