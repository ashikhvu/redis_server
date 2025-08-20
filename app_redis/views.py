from django.shortcuts import render, redirect
from .models import Order
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def home(request):
    orders = Order.objects.all()
    count = Order.objects.count()
    return render(request, "home.html", {"order": orders, "count": count})


def create(request):
    Order.objects.create(item_name="item1", qty=1, total=12)

    # notify websocket clients
    channel_layer = get_channel_layer()
    count = Order.objects.count()
    async_to_sync(channel_layer.group_send)(
        "orders",
        {"type": "order_update", "count": count}   # ✅ send count
    )

    return redirect("home")


def delete_all(request):
    Order.objects.all().delete()

    # notify websocket clients (count will be 0)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "orders",
        {"type": "order_update", "count": 0}   # ✅ reset count
    )

    return redirect("home")
