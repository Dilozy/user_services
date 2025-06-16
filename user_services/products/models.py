from django.db import models
from django.conf import settings


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = "pending", "Ожидает оплаты"
        PAID = "paid", "Оплачен"
        PACKING = "packing", "В сборке"
        DELIVERING = "delivering", "Доставляется"
        COMPLETED = "completed", "Выполнен"
        
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="my_orders",
                             verbose_name="Пользователь",
                             null=True, blank=True)
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    email = models.EmailField(verbose_name="Email")
    address = models.TextField(verbose_name="Адрес")
    city = models.CharField(max_length=100,
                            verbose_name="Город")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False, verbose_name="Оплачен")
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        verbose_name="Статус заказа"
    )

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"])
        ]
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Order: {self.id}"


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Наименование", db_index=True)
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name="Цена")

    class Meta:
        ordering = ["name"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name="items")
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name="order_products")
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    @property
    def cost(self):
        return self.price * self.quantity
