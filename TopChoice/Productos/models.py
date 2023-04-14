from django.db import models
from Categorias.models import Category,SubCategory
from django.urls import reverse
from Usuario.models import *
from django.db.models import Avg, Count

#modelo de los productos
class Products(models.Model):
    product_id = models.AutoField(unique=True,primary_key=True)
    product_name = models.CharField(max_length=50,db_index=True)
    slug = models.CharField(max_length=100,unique=True,db_index=True)
    description = models.CharField(max_length=300)
    price = models.IntegerField()
    product_image_stock = models.ImageField(upload_to='photos/products/stock')
    product_image_secundary = models.ImageField(upload_to='photos/products/secundary',null=True,blank=True)
    product_image_extra = models.ImageField(upload_to='photos/products/extra',null=True,blank=True)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def get_url(self): #devuelve una url para poder ver el detalle mas adelante
        return reverse('product_information',args=[self.category.slug,self.slug])
    
    def __str__(self):
        return self.product_name
    
    def averageRating(self):
        comments = Comments.objects.filter(product=self, is_available=True).aggregate(average=Avg('rating'))
        avg=0
        if comments['average'] is not None:
            avg = float(comments['average'])
        return avg
    
    def countRating(self):
        comments = Comments.objects.filter(product=self, is_available=True).aggregate(count=Count('id'))
        count = 0
        if comments['count'] is not None:
            count = int(comments['count'])
            
        return count

class Comments(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100,blank=True)
    comment = models.CharField(max_length=255,blank=True)
    rating = models.IntegerField()
    ip = models.CharField(max_length=20,blank=True)
    is_available = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title