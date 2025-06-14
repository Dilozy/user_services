from django.db import transaction

from .models import Product, OrderItem


def create_or_update_existing_order_items(products_count, order):
    products = Product.objects.order_by("?")[:products_count]
    create_items = []
    update_items = []
    
    for product in products:
        if (order_item := OrderItem.objects.filter(product=product, order=order).first()):
            order_item.quantity += 1
            update_items.append(order_item)
        else:
            create_items.append(OrderItem(order=order,
                                          product=product,
                                          price=product.price))
    
    with transaction.atomic():
        if create_items:
            OrderItem.objects.bulk_create(create_items)
        if update_items:
            OrderItem.objects.bulk_update(update_items, ["quantity"])
