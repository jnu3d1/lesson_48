from django.urls import path

from webapp.views import index, product_view

urlpatterns = [
    path('', index, name='index'),
    path('product/<int:pk>/', product_view, name='product_view'),
]
