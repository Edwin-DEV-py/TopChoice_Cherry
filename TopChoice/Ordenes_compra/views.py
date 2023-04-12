from django.shortcuts import render,redirect
from Carrito.models import *
from .forms import *
from .models import *
import datetime
import json
import math

def payment(request):
    
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_note=body['orderID'])
    
    payment = Payment(
        user = request.user,
        id = body['transID'],
        payment_method = body['payment_method'],
        amount_id = order.order_total,
        status = body['status'] #esto lo devuelve paypal
    )
    
    payment.save()
    
    order.payment = payment #le colocamos el valor de payment al atributo de payment en la clase order
    order.is_ordered = True #ahora la orden cambia a aceptado
    order.save()
    
    #registrar los items en la tabla de productos por cada compra
    items = Cart_item.objects.filter(user=request.user)
    
    #obbtenemos los datos
    for item in items:
        product = Product_order()
        product.order_id = order.order_id
        product.payment = payment
        product.user_id = request.user.pk
        product.product_id = item.product.product_id
        product.quantity = item.quantity
        product.product_price = item.product.price
        product.ordered = True
        product.save()
        
    return render(request,'tienda/pagos.html')

# Crear orden
def order(request,total=0,quantity = 0):
    
    user = request.user
    
    iva = 0
    final = 0
    
    items = Cart_item.objects.filter(user=user)
    count = items.count()
    if count <= 0:
        return redirect('store')
    
    for item in items:
        total += (item.product.price * item.quantity)
        quantity += item.quantity
        
    if request.user.is_authenticated and request.user.is_admin:
            discount = request.user.discount/100
            final = total*(1-discount)   
    elif request.user.is_authenticated:
        final = total
    
    iva = math.trunc((5*total)/100)
    final = final + iva
    dolares = round(final/4500,2)
    
    if request.method == 'POST':
        form = Orden_Form(request.POST)
        
        #capturamos los valores que necesitamos
        if form.is_valid():
            data = Order()
            data.user = user
            data.user_name = form.cleaned_data['user_name']
            data.phonenumber = form.cleaned_data['phonenumber']
            data.email = form.cleaned_data['email']
            data.address_1 = form.cleaned_data['address_1']
            data.address_2 = form.cleaned_data['address_2']
            data.departament = form.cleaned_data['departament']
            data.city = form.cleaned_data['city']
            data.country = form.cleaned_data['country']
            data.iva = iva
            data.order_total = final
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            
            #generamos eel numero de factura con la fecha de solicitud
            year = int(datetime.date.today().strftime('%Y'))
            mont = int(datetime.date.today().strftime('%m'))
            day = int(datetime.date.today().strftime('%d'))
            
            date = datetime.date(year,mont,day)
            this_date = date.strftime("%Y%m%d")
            
            id = this_date + str(data.order_id)
            data.order_note = id
            data.save()
            
            order = Order.objects.get(user=user, is_ordered=False,order_note=id)
            context = {
                'order':order,
                'items':items,
                'total':total,
                'iva':iva,
                'final':final,
                'dolares':dolares
            }
            
            return render(request,'tienda/pagos.html',context)
    else:
        return redirect('shipping_address')


