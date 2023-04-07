from .models import *
from .views import _cart_id

def counter(request):
    count = 0
    
    try:
        cart = Cart.objects.filter(cart_id=_cart_id(request))
        items = Cart_item.objects.all().filter(cart=cart[:1]) #me trae un elemento en ves de todo el array
        #esto obtiene la cantidad de cada producto
        for item in items:
            count += item.quantity
    except Cart.DoesNotExist:
        count = 0
    
    return dict(count=count)

