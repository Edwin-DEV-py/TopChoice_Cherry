from django.contrib import admin
from .models import *

class Cart_Admin(admin.ModelAdmin):
    list_display = ('cart_id','date_added')

class Cart_Item_Admin(admin.ModelAdmin):
    list_display = ('product','cart', 'quantity', 'is_active')



admin.site.register(Cart, Cart_Admin)
admin.site.register(Cart_item, Cart_Item_Admin)
