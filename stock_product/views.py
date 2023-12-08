from django.shortcuts import render

from django_filters import rest_framework as filters

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from .models import Product, Stock, StockProduct
from .serializers import ProductSerializer, StockSerializer, ProductPositionSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    search_fields = ['title', 'description']
    filter_backends = [SearchFilter]


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    search_fields = ['address']
    filterset_fields = ['products']
    filter_backends = [SearchFilter, filters.DjangoFilterBackend]


class ProductPositionSerializer(ModelViewSet):
    queryset = StockProduct
    serializer_class = ProductPositionSerializer