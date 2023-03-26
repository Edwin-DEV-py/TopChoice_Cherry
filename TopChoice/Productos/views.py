from django.shortcuts import render,get_object_or_404
from .models import *
from Categorias.models import Category

def store(request, category_slug=None):
    
    categorys = None
    products = None
    
    #validamos que los poroductos sean desplegados en una categoria o esten mezclados
    if category_slug != None:
        categorys = get_object_or_404(Category,slug=category_slug)
        products = Products.objects.filter(category=categorys,is_available=True)
        count = products.count()
    else:      
        products = Products.objects.all().filter(is_available=True)
        count = products.count()
        
    context = {
        'products':products,
        'count':count,
    }
    
    return render(request,"tienda/tienda.html",context)


def product_information(request,category_slug,product_slug):
    #validamos que el producto exista
    try:
        product_information = Products.objects.get(category__slug=category_slug, slug=product_slug)#las dos __ es una nomenclatura que obtiene el valor del campo de una estructura 
    except Exception as e:
        raise e
    
    context = {
        'product_information':product_information,
    }
    
    return render(request,'tienda/detalle.html',context)
