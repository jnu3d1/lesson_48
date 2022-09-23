from django.urls import path

from api_1.views import *

app_name = 'api_1'

urlpatterns = [
    path('products/', ProductView.as_view()),
    path('products/<int:pk>/', ProductView.as_view()),
]