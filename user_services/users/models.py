from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    phone_regex = RegexValidator(regex=r"^((\+7)|8)\d{10}$",
                                 message="Номер телефона должен быть в формате " \
                                 "+79999999999 или 89999999999" 
                                 )
    
    phone = models.CharField(max_length=12, unique=True,
                             validators=[phone_regex],
                             )
    # заполняется сервисом bot при регистрации
    telegram_chat_id = models.IntegerField(null=True, blank=True)

    REQUIRED_FIELDS = ["email", "phone"]
