from .models import *
from .views import _cart_id

def counter(request):
    cart_count = 0
    
    try:
        cart = Cart.objects.filter(cart_id=_cart_id(request))
        
        if request.user.is_authenticated:
            items = Cart_item.objects.all().filter(user=request.user)
        else:                
            items = Cart_item.objects.all().filter(cart=cart[:1]) #me trae un elemento en ves de todo el array
        #esto obtiene la cantidad de cada producto
        for item in items:
            cart_count += item.quantity
    except Cart.DoesNotExist:
        cart_count = 0
    
    return dict(cart_count=cart_count)

