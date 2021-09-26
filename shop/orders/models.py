from typing import Optional, Iterable

from django.db import models
from django.db.models import signals

from products.models import Product


class Status(models.Model):
    name = models.CharField(max_length=24, blank=True, null=True, default=None)
    is_active = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Order(models.Model):
    total_price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    customer_name = models.CharField(max_length=50, verbose_name='Заказчик')
    customer_email = models.EmailField(blank=True, null=True, default=None)
    customer_phone = models.CharField(max_length=48, blank=True, null=True, default=None)
    customer_address = models.CharField(max_length=128, blank=True, null=True, default=None)
    comments = models.TextField(blank=True, null=True, default=None)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Заказ {self.id} {self.status}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE, blank=True, null=True,
                              default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, default=None)
    qty = models.IntegerField(default=1)
    price_per_item = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    total_price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Заказ {self.product.name}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def save(self, *args, **kwargs) -> None:
        price_per_item = self.product.price
        self.price_per_item = price_per_item
        self.total_price = self.qty * price_per_item
        super().save(*args, **kwargs)


def product_in_order_post_save(sender, instance, created, **kwargs):
    order = instance.order
    all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)

    order_total_price = 0
    for product in all_products_in_order:
        order_total_price += product.total_price
    instance.order.total_price = order_total_price
    instance.order.save(force_update=True)


signals.post_save.connect(product_in_order_post_save, sender=ProductInOrder)
