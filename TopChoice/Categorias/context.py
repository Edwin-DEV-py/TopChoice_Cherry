from .models import *

#crea los links para usarlos a la hora de filtrar por categorias a los productos
def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)