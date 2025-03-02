from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

class Order(models.Model):
    ORDER_TYPES = [
        ("buy", "Buy"),
        ("sell", "Sell"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled")
    ]

    trader = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_type = models.CharField(max_length=4, choices=ORDER_TYPES, default="buy")
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trader.username} - {self.order_type.upper()} {self.quantity} {self.product.name} at ${self.price}"

class ExpiredOrderLog(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, default=1)
    trader = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "expired_orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name = "expired_orders")
    order_type = models.CharField(max_length=4, choices=Order.ORDER_TYPES, default="buy")
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    expired_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Expired Order: {self.trader.username} - {self.order_type.upper()} {self.quantity} {self.product.name}"
