import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Order

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("orders", self.channel_name)
        await self.accept()

        # Send initial data
        await self.send_orders()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("orders", self.channel_name)

    async def receive(self, text_data):
        # Refresh data if frontend requests
        await self.send_orders()

    async def order_update(self, event):
        # Triggered when new order is added
        await self.send_orders()

    @staticmethod
    async def get_orders():
        qs = await sync_to_async(list)(Order.objects.all().values("item_name", "qty", "total"))
        return qs

    async def send_orders(self):
        orders = await self.get_orders()
        count = len(orders)
        await self.send(text_data=json.dumps({
            "count": count,
            "orders": orders
        }))
