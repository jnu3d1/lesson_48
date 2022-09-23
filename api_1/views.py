from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api_1.serializers import ProductModelSerializer
from webapp.models import Product


# Create your views here.

class ProductView(APIView):
    serializer_class = ProductModelSerializer

    def get(self, request, *args, **kwargs):
        if self.kwargs:
            product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
            projects_data = self.serializer_class(product).data
            return Response(projects_data)
        else:
            product = Product.objects.all()
            projects_data = self.serializer_class(product, many=True).data
            return Response(projects_data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def put(self, request, *args, pk, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        serializer = self.serializer_class(data=request.data, instance=product)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        product.delete()
        return JsonResponse({'message': 'Товар удалён'})