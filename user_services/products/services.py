from django.db import transaction

from .models import Product, OrderItem


def create_or_update_existing_order_items(products_count, order):
    products = Product.objects.order_by("?")[:products_count]
    order_items = {
        order_item.product: order_item for order_item in OrderItem.objects.filter(order=order)
        }
    create_items = []
    update_items = []
    
    for product in products:
        if product in order_items:
            order_item = order_items[product]
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
