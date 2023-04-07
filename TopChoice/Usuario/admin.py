from django.contrib import admin
from .models import *

class User_admin(admin.ModelAdmin):
    list_display = ('name','email','last_login','date_joined','is_active')

admin.site.register(User,User_admin)
