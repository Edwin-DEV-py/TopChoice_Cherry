from django.db import models
from django.urls import reverse

class Category(models.Model):
    category_name = models.CharField(max_length=50,unique=True,primary_key=True)
    description = models.CharField(max_length=100,null=False)
    slug = models.CharField(max_length=100,unique=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categorys'
        
    def get_url(self):
        return reverse('product_per_category',args=[self.slug])
    
    def __str__(self):
        return self.category_name
