from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import FinanceRecord, SubCategory, Category
from .forms import FinanceRecordForm
from django.shortcuts import render

def home(request):
    return render(request, 'finance/record_list.html')

class FinanceRecordListView(ListView):
    model = FinanceRecord
    template_name = 'finance/record_list.html'
    context_object_name = 'records'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        
        status = self.request.GET.get('status')
        type_ = self.request.GET.get('type')
        category = self.request.GET.get('category')
        subcategory = self.request.GET.get('subcategory')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if status:
            queryset = queryset.filter(status=status)
        if type_:
            queryset = queryset.filter(type=type_)
        if category:
            queryset = queryset.filter(subcategory__category__id=category)
        if subcategory:
            queryset = queryset.filter(subcategory__id=subcategory)
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['subcategories'] = SubCategory.objects.all()
        context['statuses'] = FinanceRecord._meta.get_field('status').choices
        context['types'] = FinanceRecord._meta.get_field('type').choices
        return context


class FinanceRecordCreateView(CreateView):
    model = FinanceRecord
    form_class = FinanceRecordForm
    template_name = 'finance/record_form.html'
    success_url = reverse_lazy('record-list')


class FinanceRecordUpdateView(UpdateView):
    model = FinanceRecord
    form_class = FinanceRecordForm
    template_name = 'finance/record_form.html'
    success_url = reverse_lazy('record-list')


class FinanceRecordDeleteView(DeleteView):
    model = FinanceRecord
    template_name = 'finance/record_confirm_delete.html'
    success_url = reverse_lazy('record-list')
