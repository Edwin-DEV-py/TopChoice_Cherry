from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from Carrito.models import *
from Carrito.views import _cart_id
from Categorias.models import Category
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import *

#muestra los productos ya sea todos o filtrados, con una paginacion para evitar sobrecargar la DB
def store(request, category_slug=None):
    
    categorys = None
    products = None
    
    #validamos que los poroductos sean desplegados en una categoria o esten mezclados
    if category_slug != None:
        categorys = get_object_or_404(Category,slug=category_slug)
        products = Products.objects.filter(category=categorys,is_available=True).order_by('product_name')#aqui tambien podria ser por id
        pagination = Paginator(products,12)
        page = request.GET.get('page',1)
        page_x_products = pagination.get_page(page)
        num_pages = pagination.num_pages
        start = max(1, int(page)-2)
        end = min(num_pages,int(page)+2)
        if start == 1:
            end = min(5, num_pages)
        elif end == num_pages:
            start = max(num_pages - 4,1)
        page_range = range(start,end+1)
        count = products.count()
    else:      
        products = Products.objects.all().filter(is_available=True).order_by('product_name')#aqui tambien podria ser por id
        pagination = Paginator(products,12)
        page = request.GET.get('page',1)
        page_x_products = pagination.get_page(page)
        num_pages = pagination.num_pages
        start = max(1, int(page)-2)
        end = min(num_pages,int(page)+2)
        if start == 1:
            end = min(5, num_pages)
        elif end == num_pages:
            start = max(num_pages - 4,1)
        page_range = range(start,end+1)
        count = products.count()
        
    context = {
        'products':page_x_products,
        'page_range':page_range,
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

#acceso al invenatario de productos
@login_required
@user_passes_test(lambda user: user.employe_roll or user.is_admin,login_url='login')
def inventary(request):
    products = Products.objects.all()
    pagination = Paginator(products,20)
    page = request.GET.get('page',1)
    page_x_products = pagination.get_page(page)
    num_pages = pagination.num_pages
    start = max(1, int(page)-2)
    end = min(num_pages,int(page)+2)
    if start == 1:
        end = min(5, num_pages)
    elif end == num_pages:
        start = max(num_pages - 4,1)
    page_range = range(start,end+1)
    context = {'products':page_x_products,'page_range':page_range}
    return render(request,'administracion/inventario.html',context)

def edit_inventary(request,product_id):
    product = Products.objects.get(product_id=product_id)
    if request.method == 'GET':
        form = Product_Form(instance=product)
        context = {'form':form, 'product':product}
    else:
        form = Product_Form(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('inventary')
    return render(request,'administracion/editar_productos.html',context)
