from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/orders/", consumers.OrderConsumer.as_asgi()),  # 👈 trailing slash matters
]


# from django.urls import re_path
# from . import consumers

# websocket_urlpatterns = [
#     re_path(r"ws/orders/$", consumers.OrderConsumer.as_asgi()),
# ]
