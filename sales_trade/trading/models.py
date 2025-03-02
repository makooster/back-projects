from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

class Transaction(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buy_transactions")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sell_transactions")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name = "transactions")
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction: {self.buyer.username} bought {self.quantity} {self.product.name} from {self.seller.username}"
