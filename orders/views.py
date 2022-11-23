from rest_framework.generics import CreateAPIView
from .serializers import OrderItemSerializer, OrderSerializer
from .models import Order, OrderItem
from rest_framework import viewsets


class OrderItemCreateAPI(CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items").all()
    serializer_class = OrderSerializer
