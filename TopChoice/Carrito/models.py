from django.db import models
from Productos.models import *
from Usuario.models import *

#modelo que representa al carrito de compra
class Cart(models.Model):
    cart_id = models.AutoField(unique=True,primary_key=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    #el metodo str le indica a Django que imprimir cuando se necesita imprimir una isntancia de un modelo
    def __str__(self):
        return self.cart_id

#modelo que representa los elementos del carrito 
class Cart_item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    def sub_total(self):
        return self.product.price * self.quantity
    
    def __unicode__(self):
        return self.product
