from rest_framework import serializers
from django.db.models import Count

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
    class Meta:
        model = Order
        exclude = ["user"]
        read_only_fields = ["status", "paid"]


class ListRetrieveDeleteOrderSerializer(OrderSerializer):
    items = ItemsSerializer(read_only=True, many=True, source="prefetched_items")
    total_price = serializers.DecimalField(max_digits=10,
                                           decimal_places=2,
                                           read_only=True)


class UpdateOrderSerializer(OrderSerializer):
    to_add_amount = serializers.IntegerField(required=False,
                                      write_only=True,
                                      label="Добавить (кол-во)")
    to_remove_id = serializers.IntegerField(required=False,
                                         write_only=True,
                                         label="Удалить (id продукта)")
    items = ItemsSerializer(read_only=True, many=True, source="prefetched_items")
    total_price = serializers.DecimalField(max_digits=10,
                                           decimal_places=2,
                                           read_only=True)

    def validate(self, data):
        if "to_remove_id" in data:
            target_item = self.__validate_to_remove_id(data["to_remove_id"])
            data["target_item"] = target_item
        
        if "to_add_amount" in data:
            self.__validate_to_add_amount(data["to_add_amount"])
        
        return data
    
    def __validate_to_add_amount(self, value):
        total_products_in_db = Product.objects.all().aggregate(count=Count("id"))["count"]
            
        if value > total_products_in_db:
            raise serializers.ValidationError(
                {"error": f"Нельзя добавить продуктов больше, чем есть в базе ({total_products_in_db})"}
                )
    
    def __validate_to_remove_id(self, value):
        order_id = self.context["order_id"]

        order_items = OrderItem.objects.filter(order__id=order_id)
        target_item = order_items.filter(product__id=value) \
                                    .first()
        
        if not target_item:
            raise serializers.ValidationError(
                {"error": "Продукта с таким id нет в заказе"}
            )
        
        if order_items.count() == 1:
            raise serializers.ValidationError({
                "error": "Невозможно удалить последний товар из заказа. "
                "Воспользуйтесь методом DELETE для удаления"})
        
        return target_item
    
    def update(self, instance, validated_data):
        if "to_add_amount" in validated_data:
            create_or_update_existing_order_items(
                validated_data["to_add_amount"],
                instance
                )
        
        if "to_remove_id" in validated_data:
            validated_data["target_item"].delete()

        return super().update(instance, validated_data)


class CreateOrderSerializer(OrderSerializer):
    products_count = serializers.IntegerField(label="Количество продуктов",
                                              write_only=True)

    def validate_products_count(self, value):
        total_products_in_db = Product.objects.all().aggregate(count=Count("id"))["count"]
        
        if value > total_products_in_db:
            raise serializers.ValidationError(
                {"error": f"Нельзя добавить продуктов больше, чем есть в базе ({total_products_in_db})"}
                )
        
        return value
    
    def create(self, validated_data):
        user = self.context["request"].user
        products_count = validated_data.pop("products_count")

        new_order = Order.objects.create(**validated_data,
                                         user=user)
        create_or_update_existing_order_items(products_count,
                                              new_order)
        
        if user.telegram_chat_id:
            send_new_order_notification.delay(user.telegram_chat_id)
        
        return new_order


class OrderSerializerClassFactory:
    def __init__(self, request_method):
        self.request_method = request_method

    def get_serializer_class(self):
        if self.request_method in ("GET", "DELETE"):
            return ListRetrieveDeleteOrderSerializer
        if self.request_method in ("PUT", "PATCH"):
            return UpdateOrderSerializer
        return CreateOrderSerializer
