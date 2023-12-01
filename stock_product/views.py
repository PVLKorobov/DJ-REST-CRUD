from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from .models import Product, Stock, Warehouse
from .serializers import ProductSerializer, WarehouseSerializer, StockSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    search_fields = ['name', 'desc']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    seach_fields = ['product', 'warehouse']


class WarehouseViewSet(ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    search_fields = ['name']