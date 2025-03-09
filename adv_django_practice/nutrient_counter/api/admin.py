from django.contrib import admin
from .models import Food , Consumption , HealthGoal
# Register your models here.
admin.site.register(Food)
admin.site.register(Consumption)
admin.site.register(HealthGoal)