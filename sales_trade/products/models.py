from django.db import models

# Create your models here.

class Category(models.Model):
    id = models.IntegerField
    name = models.CharField(max_length=255)

class Product(models.Model):
    id = models.BigIntegerField
    name = models.CharField(max_length=255)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.IntegerField

