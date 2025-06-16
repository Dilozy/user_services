from django.db import transaction

from .models import Product, OrderItem


def update_order_items(products_count, order):
    products = Product.objects.order_by("?")[:products_count]
    product_order_item_map = {order_item.product: order_item 
                              for order_item in order.prefetched_items}
    create_items = []
    update_items = []
    
    for product in products:
        if product in product_order_item_map:
            order_item = product_order_item_map[product]
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


def create_order_items(products_count, order):
    products = Product.objects.order_by("?")[:products_count]
    create_items = []
    
    for product in products:
        create_items.append(OrderItem(order=order,
                                      product=product,
                                      price=product.price))
    
    with transaction.atomic():
        if create_items:
            OrderItem.objects.bulk_create(create_items)
