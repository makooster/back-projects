from django.contrib import admin
from .models import FinanceRecord, Category, SubCategory
# Register your models here.

@admin.register(FinanceRecord)
class FinanceRecordAdmin(admin.ModelAdmin):
    list_display = ('date', 'get_category', 'subcategory', 'type', 'status', 'formatted_sum')
    list_filter = ('status', 'type', 'subcategory__category')
    search_fields = ('comment',)
    ordering = ('-date',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
