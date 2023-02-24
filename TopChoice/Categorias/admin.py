from django.contrib import admin
from .models import *

# autocompleta el slug con el nombre de la categoria en la pagina admin

class Category_admin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name','slug')
    
admin.site.register(Category,Category_admin)
