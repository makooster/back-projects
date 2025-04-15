from django.db import models
from datetime import datetime
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
import locale
locale.setlocale(locale.LC_ALL, '')

class StatusChoices(models.TextChoices):
    BUSINESS = 'BUSINESS', 'Бизнес'
    PERSONAL = 'PERSONAL','Личное'
    TAX = 'TAX', 'Налог'
    
class TypeChoices(models.TextChoices):
    REPLENISHMENT = 'REPLENISHMENT', 'Пополнение'
    WITHDRAW = 'WITHDRAW', 'Снятие'

class Category(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

    
class SubCategory(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name= "subcategories")

    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class FinanceRecord(models.Model):

    class Meta:
        ordering = ['-date']

    date = models.DateField(_("Date"), default=datetime.today, blank=False, null=False)

    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.BUSINESS,
        null=False
    )

    type = models.CharField(
        max_length=20,
        choices=TypeChoices.choices,
        default=TypeChoices.REPLENISHMENT,
        null=False
    )

    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True, null=False)

    sum = models.PositiveBigIntegerField(default=0, blank=True, null=False)

    comment = models.TextField(max_length=1500, blank=True, null=True)

    def get_category(self):
        return self.subcategory.category
    
    def formatted_sum(self):
        return f"{self.sum:,} ₽".replace(',',' ')

    def __str__(self):
        return f"[{self.date.strftime('%d.%m.%Y')}] {self.get_type_display()} • {self.subcategory} • {self.formatted_sum()}"

