import random
from decimal import Decimal

from model_bakery import baker
from celery import shared_task

from .models import Product


@shared_task
def create_products_task():
    if not Product.objects.exists():
        baker.make(Product, _quantity=100,
                   price=lambda: Decimal(random.randint(10, 10_000)),
                   _bulk_create=True)


def create_products(sender, **kwargs):
    create_products_task.delay()
