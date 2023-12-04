from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Stock, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'name']


    def create(self, validated_data):
        positions = validated_data.pop('products')

        if type(positions) != list:
            raise ValidationError('Positions field must be a list')
        
        stock = super().create(validated_data)

        for position in positions:
            product = Product.objects.all().filter(id=position['product'])

            if not product.exists():
                raise ValidationError('Requested product does not exist')
            
            stockRecord = Stock(product=product, stock=stock, price=position['price'])
            stockRecord.save()

        return stock
    

    def update(self, instance, validated_data):
        positions = validated_data.pop('products')

        if type(positions) != list:
            raise ValidationError('Positions field must be a list')

        stock = super().update(instance, validated_data)

        stockList = stock.products.objects.all().filter(stock=stock)
        for stock in stockList:
            stock.delete()

        for position in positions:
            product = Product.objects.all().filter(id=position['product'])

            if not product.exists():
                raise ValidationError('Requested product does not exist')
            
            stockRecord = Stock(product=product, stock=stock, price=position['price'])
            stockRecord.save()

        return stock