from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Stock, Product, Warehouse


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(min_length=5)

    class Meta:
        model = Product
        fields = ['id', 'name', 'desc']


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'product', 'warehouse', 'price', 'created_at', 'updated_at']


class WarehouseSerializer(serializers.ModelSerializer):
    stock = StockSerializer(many=True)
    name = serializers.CharField(min_length=5)

    class Meta:
        model = Warehouse
        fields = ['id', 'name']

    def create(self, validated_data):
        products = validated_data.pop('products')

        if type(products) != dict:
            raise ValidationError('products field must be a dict')
        
        warehouse = super().create(validated_data)

        for id, price in products.items():
            product = Product.objects.all().filter(id=id)

            if not product.exists():
                raise ValidationError('Requested product does not exist')
            
            stockRecord = Stock(product=product, warehouse=warehouse, price=price)
            stockRecord.save()

        return warehouse
    
    def update(self, instance, validated_data):
        products = validated_data.pop('products')

        if type(products) != dict:
            raise ValidationError('products field must be a dict')

        warehouse = super().update(instance, validated_data)

        stockList = warehouse.stock.objects.all().filter(warehouse=warehouse)
        for stock in stockList:
            stock.delete()

        for id, price in products.items():
            product = Product.objects.all().filter(id=id)

            if not product.exists():
                raise ValidationError('Requested product does not exist')
            
            stockRecord = Stock(product=product, warehouse=warehouse, price=price)
            stockRecord.save()

        return warehouse