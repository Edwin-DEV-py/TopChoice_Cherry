from django.shortcuts import render,redirect
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
        item.quantity +=1 #para sabe rla cantidad de items
        item.save()
    except Cart_item.DoesNotExist:
        item = Cart_item.objects.create(
            product=product,
            quantity = 1,
            cart = cart
        )
        item.save()
    
    return redirect('shopping_cart')
    

def shopping_cart(request):
    
    return render(request, 'tienda/carrito.html')
