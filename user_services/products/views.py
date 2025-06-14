from decimal import Decimal

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch, F, Sum, ExpressionWrapper, DecimalField

from .models import Order, OrderItem
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"order_id": self.kwargs.get("pk")})
        return context
    
    def get_queryset(self):
        total_price = Sum(F("items__product__price") * F("items__quantity"))
        
        discount_price_query = ExpressionWrapper(
            total_price - 
            total_price * F("user__subscription__tariff__discount_percent") /
            Decimal(100),
            output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        
        return Order.objects.select_related("user__subscription__tariff") \
                            .prefetch_related(Prefetch(
                                    "items",
                                    queryset=OrderItem.objects.select_related("product"))
                                    ) \
                            .filter(user=self.request.user) \
                            .annotate(total_price=discount_price_query) \
                            .defer("user__last_login", "user__password",
                                   "user__first_name", "user__last_name",
                                   "user__is_superuser", "user__username", "user__email",
                                   "user__is_staff", "user__is_active", "user__date_joined",
                                   "user__phone",
                                   "user__subscription__start_date",
                                   "user__subscription__end_date",
                                   "user__subscription__tariff__name",
                                   "user__subscription__tariff__duration_in_days",
                                   "user__subscription__tariff__description")
