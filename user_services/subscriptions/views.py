from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser

from .models import Tariff, UserSubscription
from .serializers import ListDetailTariffsSerializer, UserSubscriptionSerializer
from .permissions import IsSubscriber


class ListTariffsAPIView(generics.ListAPIView):
    queryset = Tariff.objects.all()
    serializer_class = ListDetailTariffsSerializer


class UserSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = UserSubscription.objects.prefetch_related("tariff") \
                                       .select_related("user")
    serializer_class = UserSubscriptionSerializer

    def get_permissions(self):
        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
            return [IsSubscriber()]
        if self.action == "list":
            return [IsAdminUser()]
        return []
