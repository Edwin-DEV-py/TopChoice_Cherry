from django.contrib import admin
from .models import *
from django.utils.html import format_html

class User_admin(admin.ModelAdmin):
    list_display = ('name','email','last_login','date_joined','is_active')
    readonly_fields = ('last_login','date_joined')

    
class Profile_admin(admin.ModelAdmin):
    def thumbnail(self,object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">').format(object.img.url)
    
    thumbnail.short = 'Imagen de perfil'
    list_display = ('thumbnail','user','city','address_1','address_2')

admin.site.register(User,User_admin)
admin.site.register(Profile,Profile_admin)
