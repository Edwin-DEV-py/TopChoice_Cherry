from django.shortcuts import render,get_object_or_404
from .models import *
from Categorias.models import Category
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

#muestra los productos ya sea todos o filtrados, con una paginacion para evitar sobrecargar la DB
def store(request, category_slug=None):
    
    categorys = None
    products = None
    
    #validamos que los poroductos sean desplegados en una categoria o esten mezclados
    if category_slug != None:
        categorys = get_object_or_404(Category,slug=category_slug)
        products = Products.objects.filter(category=categorys,is_available=True)
        pagination = Paginator(products,12)
        page = request.GET.get('page')
        page_x_products = pagination.get_page(page)
        count = products.count()
    else:      
        products = Products.objects.all().filter(is_available=True)
        pagination = Paginator(products,12)
        page = request.GET.get('page')
        page_x_products = pagination.get_page(page)
        count = products.count()
        
    context = {
        'products':page_x_products,
        'count':count,
        'categorys':categorys
    }
    
    return render(request,"tienda/tienda.html",context)

#redirige al usuario a la pagina del producto en detalle
def product_information(request,category_slug,product_slug):
    
    category = get_object_or_404(Category,slug=category_slug)
    product = Products.objects.filter(category=category,is_available=True)[:4]
    product2 = Products.objects.filter(category=category,is_available=True)[4:8]
    
    #validamos que el producto exista
    try:
        product_information = Products.objects.get(category__slug=category_slug, slug=product_slug)#las dos __ es una nomenclatura que obtiene el valor del campo de una estructura 
    except Exception as e:
        raise e
    
    context = {
        'product_information':product_information,
        'product':product,
        'product2':product2
    }
    
    return render(request,'tienda/detalle.html',context)
