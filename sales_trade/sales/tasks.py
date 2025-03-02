from django.utils.timezone import now
from datetime import timedelta
from sales.models import Order, ExpiredOrderLog
from celery import shared_task

@shared_task
def auto_cancel_expired_orders():
    expiration_time = now() - timedelta(days=1) 

    expired_orders = Order.objects.filter(status="pending", created_at__lt=expiration_time)

    # Create ExpiredOrderLog entries in bulk (efficient)
    expired_logs = [
        ExpiredOrderLog(
            order=order,
            trader=order.trader,
            product=order.product,
            order_type=order.order_type,
            quantity=order.quantity,
            price=order.price
        )
        for order in expired_orders if not ExpiredOrderLog.objects.filter(order=order).exists()
    ]
    ExpiredOrderLog.objects.bulk_create(expired_logs)

    # Bulk update orders to 'cancelled' status
    expired_orders.update(status="cancelled")

    return f"Deleted {expired_orders.count()} expired orders"
