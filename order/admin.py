from django.contrib import admin
from order.models import Order, OrderItem



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # بدون ردیف خالی اضافی
    readonly_fields = ('product', 'variant', 'quantity', 'price')
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_number', 'full_name', 'email', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'email', 'order_number')
    readonly_fields = ('order_number', 'created_at')
    inlines = [OrderItemInline]
