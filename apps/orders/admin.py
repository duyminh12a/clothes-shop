from django.contrib import admin
from .models import Order, OrderItem, PaymentTransaction

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'color_name', 'size_name', 'quantity', 'unit_base_price', 'front_print_price', 'back_print_price', 'subtotal')

class PaymentTransactionInline(admin.TabularInline):
    model = PaymentTransaction
    extra = 0
    readonly_fields = ('gateway', 'transaction_id', 'amount', 'status', 'created_at')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_code', 'customer_name', 'customer_phone', 'total_amount', 'order_status', 'payment_method', 'payment_status', 'created_at')
    list_filter = ('order_status', 'payment_method', 'payment_status', 'created_at')
    search_fields = ('order_code', 'customer_name', 'customer_phone', 'customer_email')
    inlines = [OrderItemInline, PaymentTransactionInline]
    readonly_fields = ('order_code', 'created_at', 'updated_at')
