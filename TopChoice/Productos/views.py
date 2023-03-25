from django.shortcuts import render,get_object_or_404
from .models import *
from Categorias.models import Category

def store(request, category_slug=None):
    
    categorys = None
    products = None
    
    if category_slug != None:
        categorys = get_object_or_404(Category,slug=category_slug)
        products = Products.objects.filter(category=categorys,is_available=True)
        count = products.count()
    else:      
        products = Products.objects.all().filter(is_available=True)
        count = products.count()
        
    context = {
        'products':products,
        'count':count
    }
    return render(request,"tienda/tienda.html",context)
