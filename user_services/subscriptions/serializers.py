from rest_framework import serializers

from .models import Tariff, UserSubscription


class ListDetailTariffsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = "__all__"


class UserSubscriptionSerializer(serializers.ModelSerializer):
    tariff = serializers.CharField(write_only=True, label="Тариф", required=False)
    tariff_details = ListDetailTariffsSerializer(read_only=True, source="tariff")

    class Meta:
        model = UserSubscription
        exclude = ["user"]
        read_only_fields = ["end_date", "start_date"]
    
    def validate(self, data):
        if "tariff" in data:
            try:
                data["tariff"] = Tariff.objects.get(name=data["tariff"])
            except Tariff.DoesNotExist:
                raise serializers.ValidationError({"error": "Тариф не найден"})
        
        elif self.context["request"].method == "POST" and "tariff" not in data:
            raise serializers.ValidationError({"error": "В запросе необходимо указать тариф"})
        
        return data
    
    def create(self, validated_data):
        user = self.context["request"].user
        tariff = validated_data["tariff"]
        
        new_subscription = UserSubscription(**validated_data,
                                            user=user)
        new_subscription.save(duration_in_days=tariff.duration_in_days)
        return new_subscription
