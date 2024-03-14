from django.urls import path
from .consumers import DisasterConsumer,CommunicationEnablerConsumer

websocket_urlpatterns = [
    path("disasterNOTI/", DisasterConsumer.as_asgi()),
    path('enable-communication/<str:group_name>/', CommunicationEnablerConsumer.as_asgi()),
]

