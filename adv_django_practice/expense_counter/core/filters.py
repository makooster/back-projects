import django_filters
from .models import Expense, Category


class ExpenseFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name='date', lookup_expr='exact', label="Date")
    # date = django_filters.DateFromToRangeFilter(label="Date Range")
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), label="Category")

    class Meta:
        model = Expense
        fields = ['date', 'category']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ExpenseFilter, self).__init__(*args, **kwargs)
        if user:
            self.filters['category'].queryset = Category.objects.filter(user=user) 