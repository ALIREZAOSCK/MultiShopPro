from django.contrib import admin
from .models import Order, OrderItem, DiscountCode


admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(DiscountCode)
