from django.db import models
from Categorias.models import Category
from django.urls import reverse

class Productos(models.Model):
    product_id = models.IntegerField(unique=True,primary_key=True)
    product_name = models.CharField(max_length=50)
    slug = models.CharField(max_length=100,unique=True)
    description = models.CharField(max_length=100)
    price = models.IntegerField()
    product_image_stock = models.ImageField(upload_to='photos/products/stock')
    product_image_secundary = models.ImageField(upload_to='photos/products/secundary')
    product_image_extra = models.ImageField(upload_to='photos/products/extra')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def get_url(self):
        return reverse('product_information',args=[self.category.slug,self.slug])
    
    def __str__(self):
        return self.product_name
