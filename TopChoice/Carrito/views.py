from django.shortcuts import render,redirect,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from Productos.models import *
from .models import *

#obtenemos la sesion del usuario actual dentro de la web local a traves de una funcion que trabaja a nivel de archivo
def _cart_id(request):
    
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart
    
def add(request, product_id):
    
    product = Products.objects.get(product_id=product_id)
    
    #verificamos si el carrito existe y si no lo creamos
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()
        
    #ahora agregamos los productos al carrito
    try:
        item = Cart_item.objects.get(product=product,cart=cart)
        item.quantity +=1 #para saber la cantidad de items
        item.save()
    except Cart_item.DoesNotExist:
        item = Cart_item.objects.create(
            product=product,
            quantity = 1,
            cart = cart
        )
        item.save()
    
    return redirect('shopping_cart')

#remover la cantida del item del carrito
def remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Products, product_id=product_id)
    item = Cart_item.objects.get(product=product,cart=cart)
    if item.quantity>1:
        item.quantity -=1
        item.save()
    else:
        item.delete()
    return redirect('shopping_cart')

#borrar el item del carrito
def delete(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Products, product_id=product_id)
    item = Cart_item.objects.get(product=product,cart=cart)
    item.delete()
    return redirect('shopping_cart')
    
def shopping_cart(request, total=0, quantity=0, items=None):
    
    #mostramos los productos si existen
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))#obtenemos el carrito asignado
        items = Cart_item.objects.filter(cart=cart, is_active=True) #esto es una lista de los items
        #bucle para allar el precio total de la orden
        for item in items:
            total += (item.product.price*item.quantity)
            quantity += item.quantity
            
        iva = (5*total)/100
        final = total + iva
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

def shipping_address(request):
    return render(request,'tienda/envio.html')
