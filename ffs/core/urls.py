from django.urls import path
from .views import (
    FinanceRecordListView,
    FinanceRecordCreateView,
    FinanceRecordUpdateView,
    FinanceRecordDeleteView,
)

urlpatterns = [
    path('', FinanceRecordListView.as_view(), name='record-list'),
    path('create/', FinanceRecordCreateView.as_view(), name='record-create'),
    path('edit/<int:pk>/', FinanceRecordUpdateView.as_view(), name='record-edit'),
    path('delete/<int:pk>/', FinanceRecordDeleteView.as_view(), name='record-delete'),
]
