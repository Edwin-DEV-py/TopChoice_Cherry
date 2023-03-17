from django.contrib import admin
from .models import *

class User_admin(admin.ModelAdmin):
    list_display = ('first_name','last_name','email','is_active')

admin.site.register(User,User_admin)
