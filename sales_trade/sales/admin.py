from django.contrib import admin
from .models import Order, ExpiredOrderLog
# Register your models here.

admin.site.register(Order)
admin.site.register(ExpiredOrderLog)