from django.contrib import admin
from .models import *

class order_products(admin.TabularInline):
    model = Product_order
    readonly_fields = ('payment','user','product','quantity','product_price','ordered')
    extra = 0

class oder_detail(admin.ModelAdmin):
    list_display = ['order_note','name','email','city','order_total','status','is_ordered','create_date']
    list_filter = ['status','is_ordered']
    search_fields = ['order_note','name','email']
    list_per_page = 25
    inlines = [order_products]

admin.site.register(Payment)
admin.site.register(Order,oder_detail)
admin.site.register(Product_order)
