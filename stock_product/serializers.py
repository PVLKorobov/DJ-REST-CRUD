from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Stock, Product, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']


    def create(self, validated_data):
        positions = validated_data.pop('products', [])
        
        stock = super().create(validated_data)

        for position in positions:
            product = position['product']
            
            StockProduct.objects.create(stock=stock, product=product, price=position['price'], quantity=position['quantity'])

        return stock
    

    def update(self, instance, validated_data):
        positions = validated_data.pop('products', [])

        stock = super().update(instance, validated_data)

        for position in positions:
            product = Product.objects.all().filter(id=position['product'])

            if not product.exists():
                raise ValidationError('Requested product does not exist')
            
            StockProduct.objects.update_or_create(stock=stock, product=product,
                                                  defaults={'price':position['price'],
                                                            'quantity':position['quantity']})

        return stock