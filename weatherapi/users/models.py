from django.contrib.auth.models import AbstractUser
from django.db import models
from cities.models import City

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("manager", "Manager"),
        ("user", "User"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",  
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions", 
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
