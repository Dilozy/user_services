from datetime import datetime, timedelta

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings


class Tariff(models.Model):
    name = models.CharField(max_length=30, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    discount_percent = models.PositiveIntegerField(default=0,
                                                   validators=[MaxValueValidator(100)],
                                                   verbose_name="Скидка")
    duration_in_days = models.PositiveIntegerField(default=30)
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(0)],
                                verbose_name="Цена")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"


class UserSubscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name="subscription")
    tariff = models.ForeignKey(Tariff,
                               on_delete=models.CASCADE,
                               related_name="subscriptions")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if "duration_in_days" in kwargs:
            duration_in_days = kwargs.pop("duration_in_days")
            
            self.start_date = datetime.now()
            self.end_date = self.start_date + timedelta(days=duration_in_days)
        
        super().save(*args, **kwargs)
