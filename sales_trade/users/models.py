from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework import generics, permissions

# Create your models here.

class User(AbstractUser):
    ADMIN = "admin"
    TRADER = "trader"
    SALES_REP = "sales_rep"
    CUSTOMER = "customer"

    ROLE_CHOICES = [
        (ADMIN, "Admin"),
        (TRADER, "Trader"),
        (SALES_REP, "Sales Representative"),
        (CUSTOMER, "Customer"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CUSTOMER)
    profile_pic = models.ImageField(upload_to="profile_pics/", blank=True, null=True, default="profile_pics/default.png")

    def __str__(self):
        return f"{self.username} - {self.role}"
    
