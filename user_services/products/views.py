from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch

from .models import Order
from .serializers import OrderSerializer
from subscriptions.models import UserSubscription


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"order_id": self.kwargs.get("pk")})
        return context
    
    def get_queryset(self):
        return Order.objects.all().select_related("user__subscription__tariff") \
                                  .prefetch_related("items",
                                                    "items__product") \
                                  .filter(user=self.request.user) \

