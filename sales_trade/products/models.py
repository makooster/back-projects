from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)  
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name  

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products") 
    quantity = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)  
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.name} ({self.category.name})"  
