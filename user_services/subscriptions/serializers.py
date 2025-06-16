from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from .models import Tariff, UserSubscription
from users.serializers import UserSerializer


class ListDetailTariffsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = "__all__"


class UserSubscriptionSerializer(serializers.ModelSerializer):
    tariff = serializers.CharField(write_only=True, label="Тариф")
    tariff_details = ListDetailTariffsSerializer(read_only=True, source="tariff")
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserSubscription
        fields = "__all__"
        read_only_fields = ["end_date", "start_date"]

    def validate(self, data):
        try:
            data["tariff"] = Tariff.objects.get(name=data["tariff"])
        except Tariff.DoesNotExist:
            raise serializers.ValidationError({"error": "Тариф не найден"})
        
        return data
    
    def create(self, validated_data):
        tariff = validated_data["tariff"]
        user = self.context["request"].user
        
        start_date = timezone.now()
        end_date = start_date + timedelta(days=tariff.duration_in_days)
        
        return UserSubscription.objects.create(**validated_data,
                                               user=user,
                                               start_date=start_date,
                                               end_date=end_date)

