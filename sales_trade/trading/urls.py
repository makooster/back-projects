from django.urls import path
from .views import trading_orders_list, trading_order_detail, transaction_detail, transaction_list

urlpatterns = [
    path("orders/", trading_orders_list, name="trading_orders"),
    path("orders/<int:order_id>/", trading_order_detail, name="trading_order_detail"),
    path("transactions/", transaction_list, name="transaction_list"),
    path("transactions/<int:transaction_id>/", transaction_detail, name="transaction_detail"),
]
