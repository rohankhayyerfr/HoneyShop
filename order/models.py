# orders/models.py
from django.db import models
from django.conf import settings
from store.models import Product, ProductVariant

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Wating for payment'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    session_id = models.CharField(max_length=255, blank=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=30)
    email = models.EmailField(default='')
    address = models.TextField()

    total_price = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)

    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()  # قیمت واحد در لحظه خرید

    def total_price(self):
        return self.quantity * self.price
