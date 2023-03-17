from django.db import models
from Usuario.models import *
from Productos.models import *

class Payment(models.Model):
    payment_id = models.AutoField(unique=True,primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100)
    amount_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.payment_id
    
status_content = (
    ('Nuevo','Nuevo'),
    ('Aceptado','Aceptado'),
    ('Completado','Completado'),
    ('Cancelado','Cancelado'),
)

class Order(models.Model):
    order_id = models.AutoField(unique=True,primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phonenumber = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    addres_1 = models.CharField(max_length=100)
    addres_2 = models.CharField(max_length=100)
    departament = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    iva = models.FloatField()
    status = models.CharField(max_length=20, choices=status_content, default='Nuevo')
    #anadir el campo ip
    is_ordered = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    upload_date = models.DateTimeField(auto_now=True)
    
    def name(self):
        return f'{self.first_name} {self.last_name}'
    
    def full_address(self):
        return f'{self.city} {self.addres_1} {self.addres_2}'
    
    def __str__(self):
        return self.first_name
    
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