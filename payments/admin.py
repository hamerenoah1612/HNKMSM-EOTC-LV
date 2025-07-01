
from django.contrib import admin
from .models import (
    PaymentCases,
    CartPayment,
    CartPaymentCases,
    Category,
    ShippingInformation,
    Order,
    OrderCase,
    userOrderHistory,
    
)
admin.site.register(PaymentCases)
admin.site.register(CartPayment)
admin.site.register(CartPaymentCases)
admin.site.register(Category)
admin.site.register(ShippingInformation)

# admin.site.register(Order)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user', 
        'order_id', 
        'total_amount',
        'payment_status', 
        'created_at',
        'updated_at',
    )
    search_fields = ('user',)
    
# admin.site.register(userOrderHistory)
@admin.register(userOrderHistory)
class userOrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'order_confirmation_number','status','created')
    search_fields = ('user',)

# admin.site.register(OrderCase)
@admin.register(OrderCase)
class OrderCaseAdmin(admin.ModelAdmin):
    list_display = (
        'order', 
        'payment_case',
        'shipping_information',
        'quantity',
        'total_price',
        'delivery_state',
        'created_at',
        'updated_at',
        )
    search_fields = ('order.user',)
    
