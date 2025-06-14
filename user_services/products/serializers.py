from rest_framework import serializers

from .models import Order, Product, OrderItem
from .services import create_or_update_existing_order_items
from .tasks import send_new_order_notification


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ["product", "quantity", "cost"]


class OrderSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(label="Количество продуктов",
                                              write_only=True)
    items = ItemsSerializer(read_only=True, many=True)
    total_cost = serializers.SerializerMethodField()
    to_add_amount = serializers.IntegerField(required=False,
                                      write_only=True,
                                      label="Добавить (кол-во)")
    to_remove_id = serializers.IntegerField(required=False,
                                         write_only=True,
                                         label="Удалить (id продукта)")
    
    class Meta:
        model = Order
        exclude = ["user"]
        read_only_fields = ["status", "paid"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context["request"]
        
        if request.method in ["PUT", "PATCH"]:
            self.fields.pop("products_count")
        else:
            self.fields.pop("to_add_amount")
            self.fields.pop("to_remove_id")

    def validate(self, data):
        if "to_remove_id" in data:
            try:
                order_item = OrderItem.objects.get(
                    product__id=data["to_remove_id"],
                    order=Order.objects.get(id=self.context["order_id"])
                    )
            except OrderItem.DoesNotExist:
                raise serializers.ValidationError(
                    {"error": "Продукта с таким id нет в заказе"}
                    )
            
            data["to_remove_obj"] = order_item
        
        return data

    def create(self, validated_data):
        user = self.context["request"].user
        products_count = validated_data.pop("products_count")

        new_order = Order.objects.create(**validated_data,
                                         user=user)
        create_or_update_existing_order_items(products_count,
                                              new_order)
        
        return new_order
    
    def update(self, instance, validated_data):
        if "to_add_amount" in validated_data:
            create_or_update_existing_order_items(
                validated_data["to_add_amount"],
                instance
                )
        
        if "to_remove_id" in validated_data:
            validated_data["to_remove_obj"].delete()

        return super().update(instance, validated_data)

    def get_total_cost(self, obj):
        user = self.context["request"].user
        total = sum(item.cost for item in obj.items.all())
        tariff_discount = user.subscription.tariff.discount_percent

        return total - total * tariff_discount / 100
    
    def save(self, **kwargs):
        user_chat_id = self.context["request"].user.telegram_chat_id
        if user_chat_id:
            send_new_order_notification.delay(user_chat_id)
        return super().save(**kwargs)
    
