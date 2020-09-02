from django.contrib import admin
from fasteat.models import Restaurant, FoodItem, Order, OrderDetail,  FoodCategory,UserProfile
# Register your models here.

admin.site.register(Restaurant)
admin.site.register(FoodItem)
# admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(OrderDetail)
# admin.site.register(Payment)
admin.site.register(FoodCategory)
# admin.site.register(Specification)
admin.site.register(UserProfile)
