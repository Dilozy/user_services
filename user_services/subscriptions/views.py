from rest_framework import generics, viewsets

from .models import Tariff, UserSubscription
from .serializers import ListDetailTariffsSerializer, UserSubscriptionSerializer


class ListTariffsAPIView(generics.ListAPIView):
    queryset = Tariff.objects.all()
    serializer_class = ListDetailTariffsSerializer


class UserSubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = UserSubscriptionSerializer

    def get_queryset(self):
        return UserSubscription.objects.select_related("tariff") \
                               .filter(user=self.request.user).defer("user")