from django.contrib import admin
from .models import *


#crea el slug con el nombre de los productos
class Product_admin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('product_name',)}
    list_display = ('product_name','price','stock','is_available','category','subcategory')
  
admin.site.register(Products,Product_admin)  