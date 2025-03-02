from django.shortcuts import render, get_object_or_404
from sales.models import Order
from .models import Transaction

def trading_orders_list(request):
    orders = Order.objects.all()
    return render(request, "trading/order_list.html", {"orders": orders})

def trading_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "trading/order_detail.html", {"order": order})

def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, "trading/transaction_list.html", {"transactions": transactions})

def transaction_detail(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    return render(request, "trading/transaction_detail.html", {"transaction": transaction})
