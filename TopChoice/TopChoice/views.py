from django.shortcuts import render
from Categorias.models import Category, SubCategory

#vista para la pagina principal
def header(request):
    categorias = Category.objects.all()
    context = {
        'categorias':categorias,
    }
    return render(request,'index.html',context)

def ejemplo(request):
    return render(request,'ejemplo.html')

def inicio_sesion(request):
    return render(request,'inicio_sesion.html')

def registro(request):
    return render(request,'registro.html')

