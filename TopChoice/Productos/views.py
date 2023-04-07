from django.shortcuts import render,get_object_or_404
from .models import *
from Carrito.models import *
from Carrito.views import _cart_id
from Categorias.models import Category
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

#muestra los productos ya sea todos o filtrados, con una paginacion para evitar sobrecargar la DB
def store(request, category_slug=None):
    
    categorys = None
    products = None
    
    #validamos que los poroductos sean desplegados en una categoria o esten mezclados
    if category_slug != None:
        categorys = get_object_or_404(Category,slug=category_slug)
        products = Products.objects.filter(category=categorys,is_available=True).order_by('product_name')#aqui tambien podria ser por id
        pagination = Paginator(products,12)
        page = request.GET.get('page')
        page_x_products = pagination.get_page(page)
        count = products.count()
    else:      
        products = Products.objects.all().filter(is_available=True).order_by('product_name')#aqui tambien podria ser por id
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
        cart = Cart_item.objects.filter(cart__cart_id=_cart_id(request),product=product_information).exists()#validamos que el prodcuto este en el carrito y el exists devuelve true o false
    except Exception as e:
        raise e
    
    context = {
        'product_information':product_information,
        'product':product,
        'product2':product2,
        'cart':cart
    }
    
    return render(request,'tienda/detalle.html',context)

#funcion para la barra de busqueda
def search(request):
    
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        #obtenemos el conjunto de productos que coincidan con lo escrito
        if keyword:
            products = Products.objects.order_by('product_name').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))#aqui esta el query, la | es un OR
            count = products.count()
            
    context = {
        'products':products,
        'count':count
    }
    
    return render(request, 'tienda/tienda.html',context)
    
