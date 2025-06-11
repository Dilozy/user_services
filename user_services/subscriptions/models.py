from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings


class Tariff(models.Model):
    name = models.CharField(max_length=30, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    discount_percent = models.PositiveIntegerField(default=0,
                                                   validators=[MaxValueValidator(100)],
                                                   verbose_name="Скидка")
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(0)],
                                verbose_name="Цена")
    
    
    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"


class UserSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="subscriptions")
    tariff = models.ForeignKey(Tariff,
                               on_delete=models.CASCADE,
                               related_name="subscriptions")
    
