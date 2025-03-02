from django.shortcuts import render
from .models import Order
from django.core.paginator import Paginator
from .models import Order

def order_list(request):
    orders = Order.objects.all().order_by("-created_at")  
    paginator = Paginator(orders, 10) 

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "sales/order_list.html", {"orders": page_obj})

from django.shortcuts import get_object_or_404

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "sales/order_detail.html", {"order": order})
