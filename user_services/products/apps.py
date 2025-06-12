from django.apps import AppConfig
from django.db.models.signals import post_migrate


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        from .signals import create_products

        post_migrate.connect(create_products, sender=self)
