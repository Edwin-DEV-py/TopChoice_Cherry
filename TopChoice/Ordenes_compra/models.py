from django.db import models
from Usuario.models import *
from Productos.models import *

class Payment(models.Model):
    payment_id = models.AutoField(unique=True,primary_key=True)
    id = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100)
    amount_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.id
    
status_content = (
    ('Nuevo','Nuevo'),
    ('Aceptado','Aceptado'),
    ('Completado','Completado'),
    ('Cancelado','Cancelado'),
)

class Order(models.Model):
    order_id = models.AutoField(unique=True,primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,blank=True,null=True)
    user_name = models.CharField(max_length=50)
    phonenumber = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100)
    departament = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=100,default="none")
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    iva = models.FloatField()
    status = models.CharField(max_length=20, choices=status_content, default='Nuevo')
    ip = models.CharField(blank=True,max_length=20)
    is_ordered = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    upload_date = models.DateTimeField(auto_now=True)
    
    def name(self):
        return f'{self.user_name}'
    
    def full_address(self):
        return f'{self.country} {self.departament} {self.city}'
    
    def __str__(self):
        return self.user_name
    
    def get_url(self): #devuelve una url para poder ver el detalle mas adelante
        return reverse('orden_detail',args=[self.order_note])
    
class Product_order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    upload_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product.product_name
