
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
admin.site.register(Order)
admin.site.register(OrderCase)
# admin.site.register(userOrderHistory)
@admin.register(userOrderHistory)
class userOrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'order_confirmation_number','status','created')
    search_fields = ('user',)

