from django.shortcuts import render
from Categorias.models import Category, SubCategory
from Productos.models import Products
import os
from django.http import FileResponse
from django.conf import settings

#vista para la pagina principal
def header(request):
    categorias = Category.objects.all()
    productos_top1 = Products.objects.filter(is_available=True)[30:34]
    productos_top2 = Products.objects.filter(is_available=True)[40:44]
    productos_new1 = Products.objects.filter(is_available=True).order_by('-date_created')[:4]
    context = {
        'categorias':categorias,
        'productos_top1':productos_top1,
        'productos_top2':productos_top2,
        'productos_new1':productos_new1
    }
    return render(request,'index.html',context)

def ejemplo(request):
    return render(request,'ejemplo.html')

def inicio_sesion(request):
    return render(request,'inicio_sesion.html')

def registro(request):
    return render(request,'registro.html')

def terms_conditions(request):
    file = os.path.join(settings.MEDIA_ROOT, 'tc.pdf')
    return FileResponse(open(file,'rb'),as_attachment=True)

