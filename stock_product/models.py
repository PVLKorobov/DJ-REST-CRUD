from django.db import models

from datetime import datetime


class Product(models.Model):
    name = models.CharField(max_length=30, unique=True)
    desc = models.CharField(max_length=400, blank=True)

class Warehouse(models.Model):
    name = models.CharField(max_length=30, unique=True)

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stock')
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        super().save(*args, **kwargs)