# orders/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),

    path(
        'paypal/create/<int:order_id>/',
        views.create_paypal_order,
        name='create_paypal_order'
    ),

    path(
        'paypal/capture/<int:order_id>/',
        views.capture_paypal_order,
        name='capture_paypal_order'
    ),

    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/failed/', views.payment_failed, name='payment_failed'),
    path('payment/<int:order_id>/', views.payment, name='payment'),
]
