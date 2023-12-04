from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from .models import Product, Stock, StockProduct
from .serializers import ProductSerializer, StockSerializer, ProductPositionSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    search_fields = ['title', 'description']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    seach_fields = ['address', 'warehouse']


class ProductPositionSerializer(ModelViewSet):
    queryset = StockProduct
    serializer_class = ProductPositionSerializer