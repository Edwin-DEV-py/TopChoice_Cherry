from django.shortcuts import render,redirect,get_object_or_404
from Carrito.models import *
from .forms import *
from .models import *
import datetime
import json
import math
from Productos.models import *
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.http import JsonResponse

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
        
        #le quitamos stock al producto
        product_stock = Products.objects.get(product_id=item.product.product_id)
        product_stock.stock -= item.quantity
        product_stock.save()
        
    #eliminamos el carrito de compra
    Cart_item.objects.filter(user=request.user).delete()
        
    #generar el correo de la factura
    mail = 'Gracias por tu compra'
    body = render_to_string('tienda/factura.html',{
        'user':request.user,
        'order':order,
        'items':items
    })
    user_email = request.user.email
    send_mail = EmailMessage(
        mail,body,settings.EMAIL_HOST_USER,to=[user_email]
    )
    send_mail.from_email = False
    send_mail.send()
    
    data = {
        'order_note':order.order_note,
        'transID':payment.payment_id
    }
    
    return JsonResponse(data)

    

# Crear orden
def order(request,total=0,quantity = 0):
    
    user = request.user
    
    iva = 0
    final = 0
    subfinal = 0
    
    items = Cart_item.objects.filter(user=user)
    count = items.count()
    if count <= 0:
        return redirect('store')
    
    for item in items:
        total += (item.product.price * item.quantity)
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

#orden completada
def complete(request):
    note = request.GET.get('order_note')
    transID = request.GET.get('payment_id')
    try:
        order = Order.objects.get(order_note=note, is_ordered=True)
        products = Product_order.objects.filter(order_id=order.order_id)
        

        subtotal = 0
        for i in products:
            subtotal += i.product_price*i.quantity
        
        
            
        payment = Payment.objects.get(payment_id=transID)
        
        context = {
            'order': order,
            'products':products,
            'note':note,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal
        }
        
        return render(request,'tienda/completado.html',context)
    except(Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('header')
    
#mostrar cada orden del historial
def order_detail(request,order_note):
    order = get_object_or_404(Order, order_note=order_note)
    products = Product_order.objects.filter(order_id=order.order_id)
        
    subtotal = 0
    for i in products:
        subtotal += i.product_price*i.quantity
        
    context = {
        'order':order,
        'products':products,
        'subtotal': subtotal
    }
    
    return render(request, 'user/factura.html',context)
    