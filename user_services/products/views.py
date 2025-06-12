from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Order
from .serializers import OrderSerializer
from .permission import IsOrderOwner


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().prefetch_related("items__product").defer("user")
    serializer_class = OrderSerializer
    permission_classes = [IsOrderOwner, IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"order_id": self.kwargs.get("pk")})
        return context
