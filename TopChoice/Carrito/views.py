from django.shortcuts import render,redirect,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from Productos.models import *
from .models import *
from django.contrib.auth.decorators import login_required
import math

#pagina 404 personalizada
def custom_404(request, exception):
    return render(request, 'paginas_error/login_error.html', status=404)

#obtenemos la sesion del usuario actual dentro de la web local a traves de una funcion que trabaja a nivel de archivo
def _cart_id(request):
    
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

@login_required(login_url='login')
def add(request, product_id):
    
    product = get_object_or_404(Products, product_id=product_id)
    user = request.user
    try:
        item = Cart_item.objects.get(product=product,user=user)
        item.quantity +=1
        item.save()
    except Cart_item.DoesNotExist:
        item = Cart_item.objects.create(
            product=product,
            user=user,
            quantity=1
        )
        return redirect('shopping_cart')
    
    return redirect('shopping_cart')

#remover la cantida del item del carrito
def remove(request, product_id):
    user = request.user
    product = get_object_or_404(Products, product_id=product_id)
    item = Cart_item.objects.get(product=product,user=user)
    if item.quantity>1:
        item.quantity -=1
        item.save()
    else:
        item.delete()
    return redirect('shopping_cart')

#borrar el item del carrito
def delete(request, product_id):
    user = request.user
    product = get_object_or_404(Products, product_id=product_id)
    item = Cart_item.objects.get(product=product,user=user)
    item.delete()
    return redirect('shopping_cart')
    
@login_required(login_url='login')
def shopping_cart(request, total=0, quantity=0, items=None):
    iva = 0
    final = 0
    subfinal=0
    #mostramos los productos si existen
    try:
        
        if request.user.is_authenticated:
            items = Cart_item.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))#obtenemos el carrito asignado
            items = Cart_item.objects.filter(cart=cart, is_active=True) #esto es una lista de los items
        #bucle para allar el precio total de la orden
        for item in items:
            total += (item.product.price*item.quantity)
            quantity += item.quantity
            
        if request.user.is_authenticated and request.user.is_admin:
            iva = math.trunc((5*total)/100)
            discount = request.user.discount/100
            subfinal = total+iva
            final = subfinal*(1-discount)   
        elif request.user.is_authenticated:
            iva = math.trunc((5*total)/100)
            final = total + iva
    
        final = final
    except ObjectDoesNotExist:
        pass
    
    context = {
        'total':total,
        'quantity':quantity,
        'items':items,
        'iva':iva,
        'final':final
    }
    
    return render(request, 'tienda/carrito.html',context)

@login_required(login_url='login')
def shipping_address(request,total=0, quantity=0, items=None):
    iva=0
    final=0
    subfinal=0
    try:
        
        if request.user.is_authenticated:
            items = Cart_item.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))#obtenemos el carrito asignado
            items = Cart_item.objects.filter(cart=cart, is_active=True) #esto es una lista de los items
        #bucle para allar el precio total de la orden
        for item in items:
            total += (item.product.price*item.quantity)
            quantity += item.quantity
            
        if request.user.is_authenticated and request.user.is_admin:
            iva = math.trunc((5*total)/100)
            discount = request.user.discount/100
            subfinal = total+iva
            final = subfinal*(1-discount)   
        elif request.user.is_authenticated:
            iva = math.trunc((5*total)/100)
            final = total + iva
    
        final = final
    except ObjectDoesNotExist:
        pass
    
    context = {
        'total':total,
        'quantity':quantity,
        'items':items,
        'iva':iva,
        'final':final
    }
    return render(request,'tienda/envio.html',context)
